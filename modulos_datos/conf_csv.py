from pyspark.sql import SparkSession
import os
import sys
import platform

# PREPARAR EL PROGRAMA PARA WINDOWS
if platform.system() == "Windows":
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# CREAR LA CONEXION PRINCIPAL
def crear_sesion(app_name="HeartDiseaseStreamSession"):
    spark = SparkSession.builder \
    .appName(app_name) \
    .master("local[*]") \
    .config("spark.driver.memory", "1g") \
    .config("spark.executor.memory", "1g") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
    .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark

# LEER EL CSV DE DATOS MEDICOS (apunta directamente a heart.csv, no a la carpeta)
def leer_csv(spark, BASE_DIR):
    # Ruta absoluta del archivo
    CSV_PATH = str(BASE_DIR / "inputs" / "Sin procesar" / "heart.csv")
    
    df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("sep", ",") \
        .load(CSV_PATH)
    return df
