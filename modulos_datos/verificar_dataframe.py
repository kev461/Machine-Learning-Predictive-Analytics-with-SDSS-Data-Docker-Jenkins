import sys

# COMPROBAR QUE LA INFORMACION ESTE BIEN
def verificar_datos(df):
    """
    Verifica que el DataFrame cumpla las condiciones mínimas antes de continuar con el pipeline.
    Se usa en Jenkins para detener el proceso si los datos no son válidos.
    """
    try:
        # REVISAR QUE NO ESTE VACIO
        assert df.count() > 0, "No hay datos para procesar"

        # VERIFICAR QUE EXISTAN TODAS LAS COLUMNAS REQUERIDAS POR EL MODELO
        columnas_requeridas = [
            "Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol", 
            "FastingBS", "RestingECG", "MaxHR", "ExerciseAngina", 
            "Oldpeak", "ST_Slope", "HeartDisease"
        ]
        for col in columnas_requeridas:
            assert col in df.columns, f"Falta la columna requerida: {col}"

        # REVISAR QUE NO FALTEN DATOS
        for col in columnas_requeridas:
            nulos = df.filter(df[col].isNull()).count()
            assert nulos == 0, f"Faltan datos en la columna {col}"

        # SI TODO ESTA BIEN SE AVISA
        print("Revision exitosa la informacion esta lista")

    except AssertionError as e:
        # SI HAY UN ERROR SE MUESTRA Y SE DETIENE EL PROGRAMA
        print(f"Problema encontrado: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado durante la verificacion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import os
    import sys
    from pathlib import Path
    
    # Aseguramos que las rutas funcionen en cualquier entorno

    BASE_DIR = Path(__file__).parent.parent
    sys.path.append(str(BASE_DIR))
    
    # Importamos las herramientas de carga de datos
    from modulos_datos.conf_csv import crear_sesion, leer_csv
    from config_entorno import configurar_entorno
    
    print("Iniciando pruebas de calidad del dataset...")
    configurar_entorno(BASE_DIR)
    spark = crear_sesion("DatasetVerification")
    
    try:
        # Cargamos los datos
        df = leer_csv(spark, BASE_DIR)
        # Ejecutamos la verificacion
        verificar_datos(df)
    finally:
        spark.stop()

