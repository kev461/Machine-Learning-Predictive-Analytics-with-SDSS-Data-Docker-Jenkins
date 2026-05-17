from pyspark.ml.feature import StringIndexer, VectorAssembler, OneHotEncoder
from pyspark.ml import Pipeline

# PREPARACION DE LOS PASOS DE APRENDIZAJE MEJORADOS
def preparar_etapas():
    """
    Crea las etapas del pipeline mejoradas con OneHotEncoding.
    """
    
    # 1. Variables categóricas
    cols_categoricas = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
    
    # Indexamos primero (Texto -> Indices)
    indexers = [
        StringIndexer(inputCol=col, outputCol=col + "_index", handleInvalid="keep")
        for col in cols_categoricas
    ]
    
    # Aplicamos OneHotEncoder (Indices -> Vectores Binarios)
    # Esto evita que el modelo asuma un orden falso entre categorías
    encoder = OneHotEncoder(
        inputCols=[col + "_index" for col in cols_categoricas],
        outputCols=[col + "_vec" for col in cols_categoricas]
    )
    
    # 2. Variables numéricas
    cols_numericas = ["Age", "RestingBP", "Cholesterol", "FastingBS", "MaxHR", "Oldpeak"]
    
    # 3. Combinar todo en el vector 'features'
    assembler_inputs = [col + "_vec" for col in cols_categoricas] + cols_numericas
    
    assembler = VectorAssembler(
        inputCols=assembler_inputs,
        outputCol="features",
        handleInvalid="keep"
    )
    
    # Devolvemos las etapas para el Pipeline
    return indexers + [encoder, assembler]
