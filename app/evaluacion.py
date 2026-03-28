from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, r2_score, adjusted_rand_score
import numpy as np

# Con esto revisamos cuántas veces el programa acertó al ponerle los nombres correctos a las cosas.
def evaluarClasificacion(modelo, xTest, yTest):
    predicciones = modelo.predict(xTest)
    exactitud = accuracy_score(yTest, predicciones)
    matriz = confusion_matrix(yTest, predicciones)
    return exactitud, matriz

# Aquí medimos qué tan cerca estuvieron los cálculos del programa comparados con los números reales.
def evaluarRegresion(modelo, xTest, yTest):
    predicciones = modelo.predict(xTest)
    error = mean_squared_error(yTest, predicciones)
    r2 = r2_score(yTest, predicciones)
    return error, r2

# Comprobamos si los grupos que el programa inventó coinciden con los que ya sabíamos que existían.
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