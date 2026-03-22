from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, r2_score, adjusted_rand_score
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

def evaluarClustering(predicciones, etiquetas_reales):
    """
    Calcula la precisión del clustering comparándolo con las etiquetas reales.
    """
    precision_ajustada = adjusted_rand_score(etiquetas_reales, predicciones)
    
    resultado = {
        "precision": round(precision_ajustada, 4),
        "algoritmo": "K-Means"
    }
    
    return resultado