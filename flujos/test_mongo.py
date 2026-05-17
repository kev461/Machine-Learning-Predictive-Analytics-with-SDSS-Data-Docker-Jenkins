from dotenv import load_dotenv
from pathlib import Path
import os
from pymongo import MongoClient

# CÓDIGO PARA PROBAR CONEXIÓN Y DATOS EN MONGODB
ruta_env = Path(__file__).parent.parent / ".env"
load_dotenv(ruta_env)

# CONFIGURACION DE LA BASE DE DATOS
mongo_uri = os.getenv("HEART_MONGO_URI")
mongo_db = os.getenv("HEART_MONGO_DB")
mongo_col = os.getenv("HEART_MONGO_COLECCION")

print(f"--- Probando conexión a {mongo_db} ---")

try:
    cliente = MongoClient(mongo_uri)
    db = cliente[mongo_db]
    coleccion = db[mongo_col]
    
    # Verificar conexión
    cliente.admin.command('ping')
    print("Conexión exitosa a MongoDB Atlas.")
    
    # Contar documentos
    total = coleccion.count_documents({})
    print(f"Total de registros encontrados: {total}")
    
    if total > 0:
        print("\nEjemplo del último registro procesado:")
        ultimo = coleccion.find().sort("timestamp", -1).limit(1)[0]
        
        # Mostrar campos clave
        print(f"   - Edad: {ultimo.get('Age')}")
        print(f"   - Sexo: {ultimo.get('Sex')}")
        print(f"   - Predicción: {ultimo.get('prediccion')}")
        print(f"   - Probabilidad: {ultimo.get('probabilidad', 'No encontrada')}")
        print(f"   - Fecha: {ultimo.get('timestamp')}")
    else:
        print("La colección está vacía. Verifica que el Spark Stream esté corriendo.")

    cliente.close()
except Exception as e:
    print(f"Error: {e}")