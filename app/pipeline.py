import pandas as pd

from app.cargadorDatos import cargarDatos
from app.preprocesamiento import dividirClasificacion, dividirRegresion, obtenerDatosClustering
from app.clasificacion import entrenarKNN
from app.regresion import entrenarRegresion
from app.clustering import entrenarKMeans
from app.evaluacion import evaluarClasificacion, evaluarRegresion, evaluarClustering
from app.utilidades import (
    guardarMetricas,
    encoderDatosReales,
    graficarMatrizConfusion,
    graficarClusters,
    graficarRegresion,
    guardarModelo,
    cargarModelo
)

def ejecutarPipeline(limite=5):
    dfSDSS = cargarDatos("sdss_sample.csv")

    resultados = {}

    # ===================== CLASIFICACION =====================
    xTrain, xTest, yTrain, yTest = dividirClasificacion(dfSDSS)

    modeloKNN = cargarModelo("outputs/modeloKNN.pkl")

    if modeloKNN is None:
        modeloKNN = entrenarKNN(xTrain, yTrain)
        guardarModelo(modeloKNN, "modeloKNN.pkl")

    # Predicciones
    predClas = modeloKNN.predict(xTest)

    # Métricas
    exactitud, matriz = evaluarClasificacion(modeloKNN, xTest, yTest)
    guardarMetricas({"accuracy": exactitud}, "classification.json")
    graficarMatrizConfusion(matriz)

    # DataFrame con resultados
    dfResultadoClas = xTest.copy()
    dfResultadoClas["real"] = yTest.values
    dfResultadoClas["prediccion"] = predClas

    resultados["clasificacion"] = dfResultadoClas.head(limite).to_dict(orient="records")

    # ===================== REGRESION =====================
    xTrainR, xTestR, yTrainR, yTestR = dividirRegresion(dfSDSS)

    modeloRegresion = cargarModelo("outputs/modeloRegresion.pkl")

    if modeloRegresion is None:
        modeloRegresion = entrenarRegresion(xTrainR, yTrainR)
        guardarModelo(modeloRegresion, "modeloRegresion.pkl")

    predReg = modeloRegresion.predict(xTestR)

    error, r2 = evaluarRegresion(modeloRegresion, xTestR, yTestR)
    guardarMetricas({"mse": error, "r2": r2}, "regression.json")

    graficarRegresion(yTestR, predReg)

    dfResultadoReg = xTestR.copy()
    dfResultadoReg["real"] = yTestR.values
    dfResultadoReg["prediccion"] = predReg

    resultados["regresion"] = dfResultadoReg.head(limite).to_dict(orient="records")

    # ===================== CLUSTERING =====================
    datosCluster,etiquetasreales = obtenerDatosClustering(dfSDSS)[0],obtenerDatosClustering(dfSDSS)[1]
    labelEncoderDatosReales=encoderDatosReales(etiquetasreales)

    modeloCluster = cargarModelo("outputs/modeloKMeans.pkl")

    if modeloCluster is None:
        modeloCluster = entrenarKMeans(datosCluster)
        guardarModelo(modeloCluster, "modeloKMeans.pkl")

    predCluster = modeloCluster.predict(datosCluster)

    metricasCluster = evaluarClustering(predCluster,labelEncoderDatosReales)
    guardarMetricas(metricasCluster, "clustering.json")
    
    graficarClusters(datosCluster, predCluster, etiquetasreales)

    dfResultadoCluster = datosCluster.copy()
    dfResultadoCluster["cluster"] = predCluster

    resultados["clustering"] = dfResultadoCluster.head(limite).to_dict(orient="records")

    return resultados