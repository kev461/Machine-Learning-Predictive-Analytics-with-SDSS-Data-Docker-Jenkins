import matplotlib
matplotlib.use('Agg')

import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.preprocessing import LabelEncoder


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

#============LABELENCODE PARA GRAFICAR CLUSTERING REAL=============
def encoderDatosReales(etiquetasReales):
    print(f"Primeros 5 valores originales: \n{etiquetasReales[:5]}")
    encoder = LabelEncoder()
    etiquetasReales = encoder.fit_transform(etiquetasReales)
    print(f"Primeros 5 valores codificados: \n{etiquetasReales[:5]}")
    return etiquetasReales

#============GRAFICAS=================
def graficarMatrizConfusion(matriz):
    os.makedirs("outputs", exist_ok=True)
    plt.figure()
    sns.heatmap(matriz, annot=True, fmt='d')
    plt.title("Matriz de Confusion")
    plt.savefig("outputs/matrizConfusion.png")
    plt.close()

def graficarClusters(datos, etiquetas, etiquetasReales):
    etiquetasReales=encoderDatosReales(etiquetasReales)
    os.makedirs("outputs", exist_ok=True)

    fig, axs = plt.subplots(1, 2, figsize=(12, 9))

    sc1 = axs[0].scatter(datos.iloc[:, 0], datos.iloc[:, 1], c=etiquetas, cmap="tab10", alpha=0.7)
    axs[0].set_title("Clusters generados")
    axs[0].set_xlabel("u")
    axs[0].set_ylabel("g")
    plt.colorbar(sc1, ax=axs[0], label="Cluster")

    #Etiquetas reales
    sc2 = axs[1].scatter(datos.iloc[:, 0], datos.iloc[:, 1], c=etiquetasReales, cmap="tab10", alpha=0.7)
    axs[1].set_title("Clases reales")
    axs[1].set_xlabel("u")
    axs[1].set_ylabel("g")
    plt.colorbar(sc2, ax=axs[1], label="Clase real")

    plt.tight_layout()

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