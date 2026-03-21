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
                    if (!fileExists('outputs\\modeloKNN.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloKMeans.pkl')) {

                        echo "Modelos no encontrados. Entrenando..."

                        bat '''
                        docker run --rm ^
                        -v "%WORKSPACE%:/app" ^
                        -w /app ^
                        python:3.11-slim ^
                        sh -c "pip install -r requirements.txt && PYTHONPATH=/app python run.py --train"
                        '''
                    }

                    if (!fileExists('outputs\\modeloKNN.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloKMeans.pkl')) {
                        error("Los modelos no se generaron correctamente")
                    } else {
                        echo "Modelos verificados correctamente"
                    }
                }
            }
        }

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

        stage('Ejecución principal') {
            steps {
                bat """
                docker stop sdss-container || exit 0
                docker rm sdss-container || exit 0

                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .\\app

                docker run --name sdss-container -d ^
                -v "%WORKSPACE%\\outputs:/app/outputs" ^
                -p 5000:5000 ^
                %IMAGE_NAME%:%IMAGE_TAG%
                """
            }
        }

        stage('Smoke Test') {
            steps {
                bat 'timeout /t 5 >nul & curl -f http://localhost:5000/metricas || exit 1'
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
            echo 'Pipeline completado. Artefactos guardados en Jenkins.'
        }
    }
}