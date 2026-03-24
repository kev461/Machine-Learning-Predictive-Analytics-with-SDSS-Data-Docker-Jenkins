import pandas as pd
from cargadorDatos import cargarDatos
import sys
#Valor de prueba

def pruebas():
    try:
        dfSDSS = cargarDatos("sdss_sample.csv")
        # Pruebas básicas
        assert not dfSDSS.empty, "Dataset vacío"
        assert dfSDSS.shape[1] > 0, "Sin columnas"

        #Evaluar si existe columnas target a usar
        assert "class" in dfSDSS.columns, "Falta columna target"
        assert "redshift" in dfSDSS.columns, "Falta columna target"

        assert not dfSDSS.empty, "Dataset vacío"
        print("✔ Dataset cargado correctamente")
        print(dfSDSS)
        
        #Validar nulos:
        for col in dfSDSS.columns:
            assert dfSDSS[col].notnull().all(), f"Nulos en {col}"
    except Exception as e:
        print(f"Error en dataset: {e}")
        sys.exit(1)