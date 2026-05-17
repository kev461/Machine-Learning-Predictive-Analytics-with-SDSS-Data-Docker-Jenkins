import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from collections import Counter
import numpy as np

def calcular_metricas_ml(coleccion, BASE_DIR):
    """
    Calcula métricas de desempeño del modelo comparando la etiqueta real (HeartDisease)
    contra la predicción guardada por el Stream.
    """
    # Traer registros que tengan tanto la etiqueta real (0 o 1) como la predicción
    # Ignoramos "No Aplica" porque no sirven para medir la precisión del modelo
    documentos = list(coleccion.find({
        "HeartDisease": {"$in": [0, 1, 0.0, 1.0]},
        "prediccion": {"$ne": None}
    }))

    if not documentos:
        return None

    # EXTRAER VALORES
    # Reales: 0 o 1
    reales = [doc["HeartDisease"] for doc in documentos]
    
    # Predichos: Convertir "riesgo" -> 1, "sin riesgo" -> 0
    predichos_str = [doc["prediccion"] for doc in documentos]
    predichos = [1 if p == "riesgo" else 0 for p in predichos_str]
    
    # Probabilidades (para el AUC-ROC): Tomamos la probabilidad de la clase 1 (riesgo)
    # En guardar_predicciones guardamos una lista [prob_0, prob_1]
    probs = []
    for doc in documentos:
        if "probability" in doc and isinstance(doc["probability"], list):
            probs.append(doc["probability"][1]) # Probabilidad de riesgo
        else:
            probs.append(1.0 if doc["prediccion"] == "riesgo" else 0.0)

    # CALCULAR MÉTRICAS
    metrics = {
        "total":      len(documentos),
        "accuracy":   round(accuracy_score(reales, predichos), 4),
        "precision":  round(precision_score(reales, predichos, zero_division=0), 4),
        "recall":     round(recall_score(reales, predichos, zero_division=0), 4),
        "f1":         round(f1_score(reales, predichos, zero_division=0), 4),
        "auc_roc":    round(roc_auc_score(reales, probs), 4) if len(set(reales)) > 1 else 0.0
    }

    # MATRIZ DE CONFUSIÓN
    clases = [0, 1] # 0: sin riesgo, 1: riesgo
    matriz = confusion_matrix(reales, predichos, labels=clases)

    # Gráfico con estética Obsidian Bio
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor("#0b0f1a")
    ax.set_facecolor("#0b0f1a")
    
    sns.heatmap(matriz, annot=True, fmt="d", cmap="Greens", 
                xticklabels=["Sin Riesgo", "Riesgo"], 
                yticklabels=["Sin Riesgo", "Riesgo"], ax=ax)
    
    ax.set_xlabel("Predicción del Modelo", color="#8892b0")
    ax.set_ylabel("Realidad (Dataset)", color="#8892b0")
    plt.title("Matriz de Confusión - Heart Disease", color="#64ffda", pad=20)
    plt.tight_layout()

    ruta_img = BASE_DIR / "api_flask" / "static" / "outputs" / "confusion_matrix.png"
    try:
        if not ruta_img.parent.exists():
            ruta_img.parent.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(ruta_img)
        print(f"Imagen generada con éxito en: {ruta_img}")
    except Exception as e:
        print(f"Aviso: No se pudo guardar la imagen por permisos: {e}")
    finally:
        plt.close()

    return metrics