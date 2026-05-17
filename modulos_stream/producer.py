import csv
import json
import time
from pathlib import Path
from kafka import KafkaProducer

# Configuración general
KAFKA_BROKER = "kafka:9092"        # Dirección del broker (dentro de Docker)
TOPIC        = "heart-records"     # Nombre del topic solicitado
DELAY_SEG    = 2                   # Segundos entre cada mensaje
BASE_DIR     = Path(__file__).parent.parent


def serializar(mensaje):
    return json.dumps(mensaje).encode('utf-8')

def crear_productor(broker):
    productor = KafkaProducer(
        bootstrap_servers=broker,
        value_serializer=serializar
    )
    print(f"Productor conectado al broker: {broker}")
    return productor


def buscar_archivo_test(directorio: Path):
    """
    Spark guarda el CSV en una carpeta con un nombre aleatorio como part-0000.csv
    Esta función busca ese archivo dentro del directorio de pruebas.
    """
    if not directorio.exists():
        raise FileNotFoundError(f"El directorio {directorio} no existe. ¡Debes correr main.py primero!")
        
    archivos_csv = list(directorio.glob("*.csv"))
    if not archivos_csv:
        raise FileNotFoundError(f"No se encontró ningún archivo CSV en {directorio}.")
        
    return archivos_csv[0]

def leer_csv(ruta: Path):
    """
    Lee el CSV de prueba (el 20% guardado por Spark)
    """
    filas = []
    with open(ruta, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            filas.append(dict(fila))

    print(f"CSV de prueba cargado: {len(filas)} filas encontradas en {ruta.name}")
    return filas


def publicar_mensaje(productor, topic: str, mensaje: dict):
    # Publica un mensaje en el topic de Kafka.
    productor.send(topic, mensaje)
    productor.flush() #Garantiza que el mensaje se envió al broker antes de continuar


def simular_stream(productor, ruta_csv, topic: str, delay):
    filas  = leer_csv(ruta_csv)
    total  = len(filas)

    print()
    print("=" * 50)
    print(f"Iniciando stream del dataset de pruebas hacia topic: {topic}")
    print(f"Total de registros : {total}")
    print(f"Delay por registro : {delay} segundos")
    print("=" * 50)
    print()

    for i, fila in enumerate(filas, start=1):
        publicar_mensaje(productor, topic, fila)
        print(f"[{i:03d}/{total}] Publicado → {fila}")

        if i < total:
            time.sleep(delay)

    print()
    print("=" * 50)
    print("Stream completado. Todos los registros de prueba fueron publicados.")
    print("=" * 50)


# ─────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────

def main():
    DIRECTORIO_TEST = BASE_DIR / "inputs" / "test_data"
    
    try:
        RUTA_CSV = buscar_archivo_test(DIRECTORIO_TEST)
        productor = crear_productor(KAFKA_BROKER)
        simular_stream(productor, RUTA_CSV, TOPIC, DELAY_SEG)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
    except KeyboardInterrupt:
        print("\nStream detenido por el usuario.")
    finally:
        if 'productor' in locals():
            productor.close()
            print("Productor cerrado correctamente.")


if __name__ == "__main__":
    main()