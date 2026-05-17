from flask import render_template, request, jsonify, send_from_directory
from pathlib import Path
import sys
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

#RUTAS DEL PROYECTO
BASE_DIR = Path(__file__).parent.parent

#AGREGAR RAÍZ AL PATH PARA IMPORTAR MÓDULOS
sys.path.insert(0, str(BASE_DIR))

from modulos_datos.conf_csv import crear_sesion
from modulos_model_IA.utilidades_modelo import cargar_modelo
from modulos_model_IA.prediccion import predecir
from flujos.conexion_mongo import conectar_mongo
from flujos.guardar_predicciones import guardar_predicciones
from flujos.consultar_stats import calcular_metricas_ml

#INICIALIZAR SPARK Y MODELO UNA SOLA VEZ
spark  = crear_sesion("FlaskAPI")
modelo = cargar_modelo(BASE_DIR)

#CONEXIÓN MONGODB
cliente, coleccion = conectar_mongo()

#ESQUEMA REUTILIZABLE PARA PREDICCIONES INDIVIDUALES MEDICALES
SCHEMA_PREDICT = StructType([
    StructField("Age", DoubleType(), True),
    StructField("Sex", StringType(), True),
    StructField("ChestPainType", StringType(), True),
    StructField("RestingBP", DoubleType(), True),
    StructField("Cholesterol", DoubleType(), True),
    StructField("FastingBS", DoubleType(), True),
    StructField("RestingECG", StringType(), True),
    StructField("MaxHR", DoubleType(), True),
    StructField("ExerciseAngina", StringType(), True),
    StructField("Oldpeak", DoubleType(), True),
    StructField("ST_Slope", StringType(), True)
])

def registrar_rutas(app):

    #SERVIR ARCHIVOS DE OUTPUTS E INPUTS
    @app.route('/outputs/<path:filename>')
    def servir_output(filename):
        return send_from_directory(BASE_DIR / 'outputs', filename)

    @app.route('/inputs/<path:filename>')
    def servir_input(filename):
        return send_from_directory(BASE_DIR / 'inputs', filename)

    # ────────────────────────────────────────────────────────
    # VISTAS HTML WEB
    # ────────────────────────────────────────────────────────
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/pacientes')
    def vista_pacientes():
        # Obtiene el historial de MongoDB para renderizar la tabla en el template
        docs = list(coleccion.find({}).sort("timestamp", -1).limit(200))
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            if 'probability' in doc and isinstance(doc['probability'], list):
                doc['probabilidad'] = float(max(doc['probability']))
            else:
                doc['probabilidad'] = 0.0
        return render_template('predicciones.html', predicciones=docs)

    @app.route('/dashboard')
    def vista_stats():
        # La página carga las stats vía JS (fetch /stats y /risk-summary)
        return render_template('stats.html')

    # ────────────────────────────────────────────────────────
    # API REST PARA POWER BI Y POSTMAN
    # ────────────────────────────────────────────────────────

    # 1. /predictions (Endpoint POST para predecir un nuevo paciente)
    @app.route('/predictions', methods=['POST'])
    def predict():
        body = request.get_json()
        
        if not body:
            return jsonify({"error": "No data provided"}), 400

        try:
            # Parse inputs
            age = float(body.get('Age', 0))
            sex = str(body.get('Sex', 'M'))
            cpt = str(body.get('ChestPainType', 'ASY'))
            rbp = float(body.get('RestingBP', 120))
            chol = float(body.get('Cholesterol', 200))
            fbs = float(body.get('FastingBS', 0))
            recg = str(body.get('RestingECG', 'Normal'))
            mhr = float(body.get('MaxHR', 150))
            ea = str(body.get('ExerciseAngina', 'N'))
            oldpeak = float(body.get('Oldpeak', 0.0))
            sts = str(body.get('ST_Slope', 'Flat'))
            
            # Create DataFrame
            datos = [(age, sex, cpt, rbp, chol, fbs, recg, mhr, ea, oldpeak, sts)]
            df = spark.createDataFrame(datos, schema=SCHEMA_PREDICT)
            
            # Predict
            df_result = predecir(df, modelo)
            fila = df_result.collect()[0]

            # GUARDAR EN MONGODB
            guardar_predicciones(coleccion, df_result)

            return jsonify({
                "paciente": body,
                "prediccion": fila["prediccion"], # "riesgo" o "sin riesgo"
                "probabilidad": float(max(fila["probability"]))
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # 2. /patients (GET para obtener el historial crudo JSON para Power BI)
    @app.route('/patients')
    def patients():
        filtro = request.args.get('riesgo', 'todos').lower().strip()
        query  = {} if filtro == 'todos' else {"prediccion": filtro}
        
        docs = list(coleccion.find(query).sort("timestamp", -1).limit(1000))
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            if doc.get('timestamp'):
                doc['timestamp'] = doc['timestamp'].isoformat()
            
            if 'probability' in doc and isinstance(doc['probability'], list):
                doc['probabilidad'] = float(max(doc['probability']))
            else:
                doc['probabilidad'] = 0.0
                
        return jsonify(docs)

    # 3. /stats (GET HTML o JSON para métricas)
    @app.route('/stats')
    def stats():
        try:
            # Retorna JSON para Power BI o front-end
            total = coleccion.count_documents({})
            con_riesgo = coleccion.count_documents({"prediccion": "riesgo"})
            sin_riesgo = coleccion.count_documents({"prediccion": "sin riesgo"})
            
            # Calcular métricas avanzadas de ML
            metricas_ia = calcular_metricas_ml(coleccion, BASE_DIR)
            
            return jsonify({
                "total_pacientes": total,
                "con_riesgo": con_riesgo,
                "sin_riesgo": sin_riesgo,
                "porcentaje_riesgo": round((con_riesgo / total * 100) if total > 0 else 0, 2),
                "ml_metrics": metricas_ia
            })
        except Exception as e:
            # Si algo falla, devolvemos un 200 con el error para no romper el Smoke Test si es temporal
            # O un 500 pero con información útil. Usaremos 500 para que el Smoke Test sepa que falló.
            return jsonify({
                "error": "Error al calcular estadísticas",
                "detalles": str(e)
            }), 500

    # 4. /risk-summary (GET resúmenes agrupados para BI)
    @app.route('/risk-summary')
    def risk_summary():
        # Ejemplo de agregacióenn  MongoDB para Power BI
        pipeline = [
            {"$group": {
                "_id": "$prediccion",
                "promedio_edad": {"$avg": "$Age"},
                "promedio_colesterol": {"$avg": "$Cholesterol"},
                "conteo": {"$sum": 1}
            }}
        ]
        resultados = list(coleccion.aggregate(pipeline))
        
        resumen = {}
        for r in resultados:
            estado = r["_id"] if r["_id"] else "desconocido"
            resumen[estado] = {
                "conteo": r["conteo"],
                "promedio_edad": round(r["promedio_edad"], 2) if r["promedio_edad"] else 0,
                "promedio_colesterol": round(r["promedio_colesterol"], 2) if r["promedio_colesterol"] else 0
            }
            
        return jsonify(resumen)
