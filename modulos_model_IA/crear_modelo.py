from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier
from modulos_model_IA.preparar_datos_modelo import preparar_etapas

def dividir_datos(df):
    """
    Separar los datos 80% para entrenamiento y 20% para pruebas
    """
    dftrain, dftest = df.randomSplit([0.8, 0.2], seed=42)
    return dftrain, dftest

# DEFINIR EL METODO DE APRENDIZAJE
def definir_Naive():
    # Mantenemos el nombre de la función por compatibilidad con el resto del código
    
    # SE TRAEN LOS PASOS DE PREPARACION
    etapas = preparar_etapas()
    
    # Creación del modelo GBT Optimizado
    gbt = GBTClassifier(
        featuresCol="features",
        labelCol="HeartDisease",
        maxIter=100,     
        maxDepth=6,      
        stepSize=0.1,    
        subsamplingRate=0.8, 
        seed=42
    )
    
    # SE CREA LA RUTA DE TRABAJO COMPLETA
    return Pipeline(stages=etapas + [gbt])
