pipeline {
    agent any

    environment {
        OUTPUTS = "${WORKSPACE}\\outputs"
        IMAGE_NAME = "sdsspipeline"
        IMAGE_TAG = "latest"
    }

    stages {

        // Checkout del repositorio
        stage('Checkout del repositorio') {
            steps {
                git branch: 'main', url: 'https://github.com/kev461/Machine-Learning-Predictive-Analytics-with-SDSS-Data-Docker-Jenkins.git'
            }
        }

        //Instalación de dependencias
        stage('Instalación de dependencias') {
            steps {
                // Instalación dentro de contenedor para no depender de Python en el host
                bat '''
                docker run --rm -v "%cd%:/app" python:3.11-slim ^
                sh -c "pip install --upgrade pip && pip install -r /app/requirements.txt"
                '''

            }
        }

        //Verificación redundante de modelos
        stage('Verificar modelos') {
            steps {
                script {
                    // Una sola ejecución que verifica, entrena si falta alguno y asegura existencia
                    bat """
                    docker run --rm -v %cd%:/app python:3.11-slim ^
                        python -c "import os; \
                        modelos = ['outputs/modeloClasificacion.pkl','outputs/modeloRegresion.pkl','outputs/modeloClustering.pkl']; \
                        entrenar = [not os.path.exists(m) for m in modelos]; \
                        if any(entrenar): import run; run.main(); \
                        assert all(os.path.exists(m) for m in modelos)"
                    """
                }
            }
        }

        //Pruebas básicas del dataset
        stage('Pruebas básicas del dataset') {
            steps {
                // Ejecuta run.py con flag --test para validar pipeline
                bat 'docker run --rm -v %cd%:/app python:3.11-slim python /app/run.py --test'
            }
        }

        //Ejecución del script principal
        stage('Ejecución principal') {
            steps {
                // Levantar Flask y entrenamiento principal dentro de Docker
                bat """
                docker stop sdss-container || exit 0
                docker rm sdss-container || exit 0
                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .\\app
                docker run --name sdss-container -d -v %cd%\\outputs:/app/outputs -p 5000:5000 %IMAGE_NAME%:%IMAGE_TAG%
                """
            }
        }

        //Smoke Test (comprobación de Flask)
        stage('Smoke Test') {
            steps {
                bat 'timeout /t 3 & curl -f http://localhost:5000/metricas || exit 1'
            }
        }

        //Almacenamiento de artefactos
        stage('Archivar artefactos') {
            steps {
                archiveArtifacts artifacts: 'outputs\\**\\*.*', fingerprint: true
            }
        }

    }

    post {
        always {
            echo 'Pipeline completado. Artefactos guardados en Jenkins.'
        }
    }
}