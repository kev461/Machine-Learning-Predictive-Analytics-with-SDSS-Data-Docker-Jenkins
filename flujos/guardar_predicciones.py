from datetime import datetime, timezone

# GUARDAR RESULTADOS EN MONGODB
def guardar_predicciones(coleccion, df_final):
    # RECOGER TODA LA INFORMACION DEL LOTE
    filas = df_final.collect()

    documentos = []
    for fila in filas:
        # Convertir fila a diccionario para acceso seguro
        f_dict = fila.asDict()
        
        # Extraer la probabilidad máxima como número
        prob_list = [float(p) for p in f_dict.get("probability", [0, 0])]
        probabilidad = float(max(prob_list)) if prob_list else 0.0

        # Crear documento con todas las variables médicas + resultado del modelo
        documento = {
            # Variables del paciente
            "Age":            f_dict.get("Age"),
            "Sex":            f_dict.get("Sex"),
            "ChestPainType":  f_dict.get("ChestPainType"),
            "RestingBP":      f_dict.get("RestingBP"),
            "Cholesterol":    f_dict.get("Cholesterol"),
            "FastingBS":      f_dict.get("FastingBS"),
            "RestingECG":     f_dict.get("RestingECG"),
            "MaxHR":          f_dict.get("MaxHR"),
            "ExerciseAngina": f_dict.get("ExerciseAngina"),
            "Oldpeak":        f_dict.get("Oldpeak"),
            "ST_Slope":       f_dict.get("ST_Slope"),
            # Si no existe HeartDisease (manual), guardar "No Aplica"
            "HeartDisease":   f_dict.get("HeartDisease") if f_dict.get("HeartDisease") is not None else "No Aplica",
            # Resultado del modelo
            "prediccion":     f_dict.get("prediccion"),
            "probability":    prob_list,
            "probabilidad":   probabilidad,
            "timestamp":      datetime.now(timezone.utc)
        }
        documentos.append(documento)

    # INSERTAR TODO EL LOTE DE GOLPE
    if documentos:
        coleccion.insert_many(documentos)
        print(f"Guardados {len(documentos)} registros en MongoDB.")
