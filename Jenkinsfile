pipeline {
    agent any

    environment {
        OUTPUTS = "${WORKSPACE}\\outputs"
        IMAGE_NAME = "sdsspipeline"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout del repositorio') {
            steps {
                git branch: 'main', url: 'https://github.com/kev461/Machine-Learning-Predictive-Analytics-with-SDSS-Data-Docker-Jenkins.git'
            }
        }

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

        stage('Verificar modelos') {
            steps {
                script {
                    if (!fileExists('outputs\\modeloClasificacion.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloClustering.pkl')) {

                        echo "Modelos no encontrados. Ejecutando verificación..."

                        bat '''
                        docker run --rm ^
                        -v "%WORKSPACE%:/app" ^
                        -w /app ^
                        python:3.11-slim ^
                        sh -c "set -e && pip install -r requirements.txt && PYTHONPATH=/app python /app/run.py --verificar"
                        '''
                    }

                    if (!fileExists('outputs\\modeloClasificacion.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloClustering.pkl')) {
                        error("Los modelos no se generaron correctamente")
                    } else {
                        echo "Modelos verificados correctamente"
                    }
                }
            }
        }

        stage('Prueba rápida del pipeline') {
            steps {
                bat '''
                docker run --rm ^
                -v "%WORKSPACE%:/app" ^
                -w /app ^
                python:3.11-slim ^
                sh -c "set -e && pip install -r requirements.txt && PYTHONPATH=/app python /app/run.py --verificar"
                '''
            }
        }

        stage('Build Docker') {
            steps {
                bat '''
                echo ===== BUILD =====
                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                '''
            }
        }

        stage('Run Docker (DEBUG)') {
            steps {
                bat '''
                docker stop sdss-container || exit 0
                docker rm sdss-container || exit 0

                echo ===== RUN (SIN -d PARA VER ERRORES) =====

                docker run ^
                -v "%WORKSPACE%\\outputs:/app/outputs" ^
                -p 5000:5000 ^
                %IMAGE_NAME%:%IMAGE_TAG%
                '''
            }
        }

        stage('Archivar artefactos') {
            steps {
                archiveArtifacts artifacts: 'outputs\\**\\*.*', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizado (modo debug).'
        }
    }
}