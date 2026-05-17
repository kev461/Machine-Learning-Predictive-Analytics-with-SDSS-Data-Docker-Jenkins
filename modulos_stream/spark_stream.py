from pyspark.sql import functions as F
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pyspark.sql import SparkSession
from pyspark.sql.types import (StructType, StructField, StringType,
                                DoubleType, IntegerType)
from modulos_model_IA.utilidades_modelo import cargar_modelo
from modulos_model_IA.prediccion import predecir
from flujos.conexion_mongo import conectar_mongo
from flujos.guardar_predicciones import guardar_predicciones

KAFKA_BROKER = "kafka:9092"
TOPIC        = "heart-records"

# ESQUEMA DE LOS DATOS MÉDICOS QUE LLEGAN POR KAFKA
# El producer envía todo como string (csv.DictReader), así que usamos StringType
# y hacemos cast dentro de procesar_lote
SCHEMA_KAFKA = StructType([
    StructField("Age",            StringType(), True),
    StructField("Sex",            StringType(), True),
    StructField("ChestPainType",  StringType(), True),
    StructField("RestingBP",      StringType(), True),
    StructField("Cholesterol",    StringType(), True),
    StructField("FastingBS",      StringType(), True),
    StructField("RestingECG",     StringType(), True),
    StructField("MaxHR",          StringType(), True),
    StructField("ExerciseAngina", StringType(), True),
    StructField("Oldpeak",        StringType(), True),
    StructField("ST_Slope",       StringType(), True),
    StructField("HeartDisease",   StringType(), True),
])

# LEER DATOS QUE LLEGAN POCO A POCO DESDE KAFKA
def leer_stream(spark, BASE_DIR):
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", TOPIC) \
        .option("startingOffsets", "earliest") \
        .load()
    return df

def deserializar_kafka(df):
    # CONVERTIR BYTES → JSON → COLUMNAS TIPADAS
    df_string = df.select(F.col("value").cast("string").alias("value"))
    df_json   = df_string.select(F.from_json(F.col("value"), SCHEMA_KAFKA).alias("datos"))
    df_parsed = df_json.select("datos.*")

    # Convertir columnas numéricas de string a sus tipos correctos
    df_typed = df_parsed \
        .withColumn("Age",          F.col("Age").cast(DoubleType())) \
        .withColumn("RestingBP",    F.col("RestingBP").cast(DoubleType())) \
        .withColumn("Cholesterol",  F.col("Cholesterol").cast(DoubleType())) \
        .withColumn("FastingBS",    F.col("FastingBS").cast(DoubleType())) \
        .withColumn("MaxHR",        F.col("MaxHR").cast(DoubleType())) \
        .withColumn("Oldpeak",      F.col("Oldpeak").cast(DoubleType())) \
        .withColumn("HeartDisease", F.col("HeartDisease").cast(IntegerType()))

    return df_typed

# PROCESAR UN LOTE DE DATOS
def procesar_lote(df, coleccion, modelo, idLote):
    if df.isEmpty():
        return

    print(f"Procesando lote {idLote} — {df.count()} registros")

    # PREDECIR RIESGO CARDÍACO
    df_predicho = predecir(df, modelo)

    # GUARDAR EN MONGODB
    guardar_predicciones(coleccion, df_predicho)

# INICIAR EL PROCESAMIENTO CONSTANTE
def iniciar_stream(spark, BASE_DIR):
    print("Iniciando Procesamiento en Tiempo Real — Heart Disease Stream")
    modelo = cargar_modelo(BASE_DIR)
    cliente, coleccion = conectar_mongo()

    df_stream = leer_stream(spark, BASE_DIR)
    df_stream = deserializar_kafka(df_stream)

    query = df_stream.writeStream \
        .foreachBatch(lambda df, id_lote: procesar_lote(df, coleccion, modelo, id_lote)) \
        .option("checkpointLocation", str(BASE_DIR / "outputs" / "checkpoint")) \
        .start()

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("Stream detenido.")
    finally:
        cliente.close()
        spark.stop()

# EJECUCION PRINCIPAL
if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent.parent

    from config_entorno import configurar_entorno
    configurar_entorno(BASE_DIR)

    from modulos_datos.conf_csv import crear_sesion
    spark = crear_sesion()
    iniciar_stream(spark, BASE_DIR)
