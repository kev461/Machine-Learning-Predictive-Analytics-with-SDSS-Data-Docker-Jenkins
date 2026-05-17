from pyspark.ml import PipelineModel

# GUARDAR LO APRENDIDO
def guardar_modelo(modelo, BASE_DIR):
    ruta = str(BASE_DIR / "outputs" / "modelo_heart")
    modelo.write().overwrite().save(ruta)
    print(f"Modelo guardado en: {ruta}")

# RECUPERAR LO APRENDIDO
def cargar_modelo(BASE_DIR):
    ruta = str(BASE_DIR / "outputs" / "modelo_heart")
    print(f"Cargando modelo desde: {ruta}")
    return PipelineModel.load(ruta)