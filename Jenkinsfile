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

        // Instalación de dependencias en contenedor
        stage('Instalación de dependencias') {
            steps {
                bat '''
                docker run --rm ^
                -v "%WORKSPACE%:/app" ^
                -w /app ^
                python:3.11-slim ^
                sh -c "pip install --upgrade pip && pip install -r requirements.txt"
                '''
            }
        }

        // Verificación de modelos con redundancia
        stage('Verificar modelos') {
            steps {
                script {
                    def modelosExisten =
                        fileExists('outputs\\modeloClasificacion.pkl') &&
                        fileExists('outputs\\modeloRegresion.pkl') &&
                        fileExists('outputs\\modeloClustering.pkl')

                    if (!modelosExisten) {
                        echo "Modelos no encontrados. Ejecutando entrenamiento..."

                        bat '''
                        docker run --rm ^
                        -v "%WORKSPACE%:/app" ^
                        -w /app ^
                        python:3.11-slim ^
                        sh -c "pip install -r requirements.txt && PYTHONPATH=/app python run.py"
                        '''
                    } else {
                        echo "Modelos ya existen, no se reentrena."
                    }

                    if (!fileExists('outputs\\modeloClasificacion.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloClustering.pkl')) {
                        error("ERROR: Los modelos no fueron generados correctamente")
                    } else {
                        echo "Modelos verificados correctamente"
                    }
                }
            }
        }

        // Pruebas básicas del dataset
        stage('Pruebas básicas del dataset') {
            steps {
                bat '''
                docker run --rm ^
                -v "%WORKSPACE%:/app" ^
                -w /app ^
                python:3.11-slim ^
                sh -c "pip install -r requirements.txt && PYTHONPATH=/app python run.py --test"
                '''
            }
        }

        // Ejecución del sistema con Docker
        stage('Ejecución del sistema') {
            steps {
                bat '''
                docker stop sdss-container || exit 0
                docker rm sdss-container || exit 0

                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .\\app

                docker run -d ^
                --name sdss-container ^
                -p 5000:5000 ^
                -v "%WORKSPACE%\\outputs:/app/outputs" ^
                %IMAGE_NAME%:%IMAGE_TAG%
                '''
            }
        }

        // Verificación del servicio
        stage('Smoke Test') {
            steps {
                bat 'timeout /t 5 >nul & curl -f http://localhost:5000/metricas || exit 1'
            }
        }

        // Almacenamiento de artefactos
        stage('Archivar artefactos') {
            steps {
                archiveArtifacts artifacts: 'outputs\\**\\*.*', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizado. Resultados disponibles en Jenkins.'
        }
    }
}