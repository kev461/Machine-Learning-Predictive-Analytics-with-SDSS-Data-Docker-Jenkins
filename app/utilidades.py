import matplotlib
matplotlib.use('Agg')

import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

def guardarMetricas(metricas, nombreArchivo):
    os.makedirs("outputs", exist_ok=True)
    with open(f"outputs/{nombreArchivo}", "w") as archivo:
        json.dump(metricas, archivo, indent=4)

def guardarModelo(modelo, nombreArchivo):
    os.makedirs("outputs", exist_ok=True)
    joblib.dump(modelo, f"outputs/{nombreArchivo}")

def cargarModelo(rutaArchivo):
    if os.path.exists(rutaArchivo):
        return joblib.load(rutaArchivo)
    return None

def graficarMatrizConfusion(matriz):
    os.makedirs("outputs", exist_ok=True)
    plt.figure()
    sns.heatmap(matriz, annot=True, fmt='d')
    plt.title("Matriz de Confusion")
    plt.savefig("outputs/matrizConfusion.png")
    plt.close()

def graficarClusters(datos, etiquetas):
    os.makedirs("outputs", exist_ok=True)
    plt.figure()
    plt.scatter(datos.iloc[:, 0], datos.iloc[:, 1], c=etiquetas)
    plt.title("Clusters")
    plt.savefig("outputs/clusters.png")
    plt.close()
    
def graficarRegresion(valoresReales, valoresPredichos):
    os.makedirs("outputs", exist_ok=True)
    plt.figure()
    plt.scatter(valoresReales, valoresPredichos)
    plt.xlabel("Valores Reales")
    plt.ylabel("Predicciones")
    plt.title("Regresion: Real vs Prediccion")
    plt.savefig("outputs/regresion.png")
    plt.close()