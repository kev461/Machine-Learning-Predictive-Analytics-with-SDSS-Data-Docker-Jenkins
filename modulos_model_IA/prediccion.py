from pyspark.sql import functions as F

# FUNCION PARA PREDECIR RIESGO CARDÍACO
def predecir(df, modelo):
    # EL MODELO TRANSFORMA EL DATAFRAME Y AGREGA LAS COLUMNAS prediction Y probability
    df_predicciones = modelo.transform(df)

    # GBTClassifier devuelve 0.0 = sin riesgo, 1.0 = con riesgo
    # Lo traducimos a texto legible
    df_final = df_predicciones.withColumn(
        "prediccion",
        F.when(F.col("prediction") == 1.0, "riesgo").otherwise("sin riesgo")
    )

    return df_final


# FUNCION PARA MEDIR QUE TAN BIEN FUNCIONA EL MODELO
def evaluar(df):
    from pyspark.ml.evaluation import BinaryClassificationEvaluator
    evaluador = BinaryClassificationEvaluator(
        labelCol="HeartDisease",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    auc = evaluador.evaluate(df)
    print(f"AUC del modelo: {auc:.4f}")
    return auc
