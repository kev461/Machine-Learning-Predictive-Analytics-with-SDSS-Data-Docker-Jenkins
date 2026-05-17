# HeartDiseaseStream: Pipeline de Predicción de Riesgo Cardíaco en Tiempo Real

HeartDiseaseStream es un ecosistema integrado de Big Data diseñado para la ingesta, procesamiento, almacenamiento y visualización de riesgos cardíacos a partir de flujos de datos médicos continuos. El proyecto implementa un pipeline de extremo a extremo que combina procesamiento en streaming con Apache Spark, aprendizaje automático y visualización interactiva.

## Arquitectura del Sistema
El sistema se divide en varias capas funcionales orquestadas mediante Docker Compose:

- **Capa de Ingesta (Kafka)**: Los datos médicos son enviados a un broker de Kafka (topic: `heart-records`) simulando la llegada de información de pacientes en tiempo real.
- **Capa de Procesamiento (PySpark Streaming)**: Lee los datos de Kafka, aplica un modelo de Machine Learning pre-entrenado y predice si el paciente tiene riesgo de enfermedad cardíaca.
- **Capa de Persistencia (MongoDB)**: Almacena las predicciones resultantes, incluyendo las probabilidades y marcas de tiempo para su posterior consulta.
- **Capa de Exposición (Flask API)**: API REST que permite consultar estadísticas (/stats), listar predicciones de pacientes (/patients) y realizar inferencias individuales (/predictions).
- **Capa de Visualización (Dashboard)**: Interfaz web integrada en Flask y conexión con Power BI para monitorear el estado de salud de los pacientes procesados.

## Tecnologías Utilizadas
- **Procesamiento**: Apache Spark (PySpark Streaming)
- **Mensajería**: Apache Kafka
- **Base de Datos**: MongoDB
- **Backend**: Flask (Python)
- **Visualización**: HTML/JS (Dashboard Onyx Glass) + Power BI
- **DevOps**: Docker, Docker Compose y Jenkins

## Manual de Uso

Este proyecto está preparado para integración y despliegue continuo (CI/CD) utilizando Jenkins.

### 1. Despliegue Automático con Jenkins
- **Pipeline**: El `Jenkinsfile` automatiza la construcción de la imagen `heart-disease-app`, ejecuta pruebas de conectividad y despliega los servicios.
- **Variables de Entorno**: Se configuran en Jenkins para inyectar credenciales de MongoDB y tokens de ngrok de forma segura.

### 2. Uso Local (Sin Jenkins)
1. **Configurar credenciales**: Crea un archivo `.env` basado en `.env.example`.
2. **Levantar la infraestructura**:
   ```bash
   docker-compose up --build -d
   ```

### 3. Acceso a la Aplicación
- **Dashboard Web**: `http://localhost:5000/`
- **Estadísticas API**: `http://localhost:5000/stats`
- **Túnel Público**: Si usas ngrok, la URL estará disponible en `http://localhost:4040`.

## Estructura del Proyecto
- `modulos_datos/`: Configuración de Spark y utilidades de lectura CSV.
- `modulos_model_IA/`: Entrenamiento, evaluación y lógica de predicción del modelo.
- `modulos_stream/`: Productor de Kafka y procesador Spark Streaming.
- `flujos/`: Lógica de conexión con MongoDB y cálculo de métricas.
- `api_flask/`: Servidor web y rutas de la API.
- `inputs/`: Datos de entrada (heart.csv) y datos de prueba.
- `outputs/`: Modelo entrenado y checkpoints del stream.
