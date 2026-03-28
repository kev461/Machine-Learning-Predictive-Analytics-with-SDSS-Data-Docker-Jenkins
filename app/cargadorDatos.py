import pandas as pd

# Esta función abre el archivo con la información para que el programa pueda empezar a leerla.
def cargarDatos(ruta):
    dfSDSS = pd.read_csv(ruta)
    return dfSDSS