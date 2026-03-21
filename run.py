from flask import Flask, jsonify, render_template, request, send_from_directory
import json
import os

from app.pipeline import ejecutarPipeline

aplicacion = Flask(__name__)

# ---------------- HOME ----------------
@aplicacion.route("/")
def inicio():
    limite = int(request.args.get("limite", 5))

    resultados = ejecutarPipeline(limite)

    return render_template(
        "index.html",
        clasificacion=resultados["clasificacion"],
        regresion=resultados["regresion"],
        clustering=resultados["clustering"],
        limite=limite
    )

# ---------------- EJECUTAR ----------------
@aplicacion.route("/ejecutar")
def ejecutar():
    limite = int(request.args.get("limite", 5))
    return jsonify(ejecutarPipeline(limite))

# ---------------- METRICAS ----------------
@aplicacion.route("/metricas")
def metricas():
    salida = {}

    if os.path.exists("outputs/classification.json"):
        with open("outputs/classification.json") as f:
            salida["clasificacion"] = json.load(f)

    if os.path.exists("outputs/regression.json"):
        with open("outputs/regression.json") as f:
            salida["regresion"] = json.load(f)
            
    if os.path.exists("outputs/clustering.json"):
        with open("outputs/clustering.json") as f:
            salida["clustering"] = json.load(f)

    return jsonify(salida)

# ---------------- IMAGENES ----------------
@aplicacion.route("/imagen/<nombre>")
def imagen(nombre):
    return send_from_directory("outputs", nombre)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("http://localhost:5000")
    print("http://localhost:5000/ejecutar?limite=10")
    aplicacion.run(host="0.0.0.0", port=5000)