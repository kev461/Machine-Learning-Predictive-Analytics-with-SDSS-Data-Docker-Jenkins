from pathlib import Path

# RUTA DEL PROYECTO (Raíz)
BASE_DIR = Path(__file__).parent

# CONFIGURACION DEL SISTEMA
from config_entorno import configurar_entorno
configurar_entorno(BASE_DIR) 

# CARGA DE HERRAMIENTAS
from modulos_datos.conf_csv import crear_sesion, leer_csv
from modulos_datos.paralelizacion import paralelizar
from modulos_model_IA.entrenar_modelo import entrenamiento
from modulos_model_IA.utilidades_modelo import guardar_modelo, cargar_modelo
from modulos_model_IA.crear_modelo import dividir_datos
from modulos_model_IA.prediccion import predecir

# PROCESO DE PREPARACION DE DATOS 
def pipeline(spark, BASE_DIR):
    # LECTURA DE INFORMACION
    df = leer_csv(spark, BASE_DIR)
    
    print("Distribución de la variable objetivo (HeartDisease):")
    df.groupBy("HeartDisease").count().show()
    
    # SEPARACION PARA APRENDIZAJE Y PRUEBAS (80/20)
    df_train, df_test = dividir_datos(df)
    
    # ORGANIZACION DEL TRABAJO
    df_train = paralelizar(df_train, 8)
    
    return df_train, df_test

# REVISION DE LA EXISTENCIIA DEL MODELO, SI NO EXISTE LO CREA
def comprobar_modelo(df_train, BASE_DIR):
    ruta_modelo = BASE_DIR / "outputs" / "modelo_heart"
    if ruta_modelo.exists():
        return cargar_modelo(BASE_DIR)
    else:
        modelo = entrenamiento(df_train)
        guardar_modelo(modelo, BASE_DIR)
        return modelo

# GUARDADO DE DATOS DE PRUEBA (20%) PARA EL PRODUCER
def guardar_datos_prueba(df_test, BASE_DIR):
    import shutil
    
    ruta_salida = BASE_DIR / "inputs" / "test_data"
    
    # Si la carpeta ya existe, eliminarla para sobrescribir
    if ruta_salida.exists():
        shutil.rmtree(ruta_salida)
        
    print(f"Guardando el 20% de datos de prueba en {ruta_salida}...")
    
    # Se guarda como un solo archivo CSV (coalesce(1)) para que el producer lo lea
    df_test.coalesce(1).write \
        .option("header", "true") \
        .csv(str(ruta_salida))
    print("Datos de prueba guardados exitosamente. El producer puede leerlos de esta carpeta.")

# INICIO DEL PROGRAMA
def main():
    # INICIO DE LA SESION
    spark = crear_sesion()
    
    # PREPARACION
    df_train, df_test = pipeline(spark, BASE_DIR)
    
    # OBTENCION DEL MODELO
    modelo = comprobar_modelo(df_train, BASE_DIR)
    
    # GUARDAR EL 20% PARA EL PRODUCER
    guardar_datos_prueba(df_test, BASE_DIR)
    
    # CIERRE
    spark.stop()

# EJECUCION
if __name__ == "__main__":
    main()
