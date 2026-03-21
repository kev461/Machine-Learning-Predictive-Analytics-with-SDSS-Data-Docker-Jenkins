import pandas as pd

def cargarDatos(ruta):
    dfSDSS = pd.read_csv(ruta)
    return dfSDSS