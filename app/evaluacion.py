from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, r2_score
import numpy as np

def evaluarClasificacion(modelo, xTest, yTest):
    predicciones = modelo.predict(xTest)
    exactitud = accuracy_score(yTest, predicciones)
    matriz = confusion_matrix(yTest, predicciones)
    return exactitud, matriz

def evaluarRegresion(modelo, xTest, yTest):
    predicciones = modelo.predict(xTest)
    error = mean_squared_error(yTest, predicciones)
    r2 = r2_score(yTest, predicciones)
    return error, r2

def evaluarClustering(predCluster):
    valores, conteos = np.unique(predCluster, return_counts=True)

    distribucion = dict(zip(valores.tolist(), conteos.tolist()))

    resultado = {
        "numeroClusters": len(valores),
        "distribucion": distribucion
    }

    return resultado