pipeline {
    agent any

    environment {
        OUTPUTS = "${WORKSPACE}\\outputs"
        IMAGE_NAME = "sdsspipeline"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kev461/Machine-Learning-Predictive-Analytics-with-SDSS-Data-Docker-Jenkins.git'
            }
        }

        stage('Instalar dependencias') {
            steps {
                script {
                    bat '''
                    if not exist outputs\\logs mkdir outputs\\logs
                    docker run --rm -v "%WORKSPACE%:/app" -w /app python:3.11-slim ^
                    sh -c "pip install --upgrade pip && pip install -r requirements.txt" ^
                    > outputs\\logs\\instalar_dependencias.log 2>&1
                    '''
                }
            }
        }

        stage('Verificar modelos') {
            steps {
                script {
                    if (!fileExists('outputs\\modeloClasificacion.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloClustering.pkl')) {

                        echo "Generando modelos..."
                        bat '''
                        if not exist outputs\\logs mkdir outputs\\logs
                        docker run --rm -v "%WORKSPACE%:/app" -w /app python:3.11-slim ^
                        sh -c "PYTHONPATH=/app python /app/run.py --verificar" ^
                        > outputs\\logs\\verificar_modelos.log 2>&1
                        '''
                    }
                }
            }
        }

        stage('Build Docker') {
            steps {
                script {
                    bat '''
                    if not exist outputs\\logs mkdir outputs\\logs
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% . > outputs\\logs\\docker_build.log 2>&1
                    '''
                }
            }
        }

        stage('Run Docker') {
            steps {
                script {
                    bat '''
                    if not exist outputs\\logs mkdir outputs\\logs
                    docker stop sdss-container 2>nul
                    docker rm sdss-container 2>nul
                    docker run -d --name sdss-container -v "%WORKSPACE%\\outputs:/app/outputs" -p 5000:5000 %IMAGE_NAME%:%IMAGE_TAG% > outputs\\logs\\docker_run.log 2>&1
                    '''
                }
            }
        }

        stage('Smoke Test') {
            steps {
                script {
                    bat '''
                    if not exist outputs\\logs mkdir outputs\\logs
                    set /a intentos=0
                    :loop
                    set /a intentos+=1
                    curl -f http://localhost:5000/metricas > outputs\\logs\\smoke_test.log 2>&1
                    if %errorlevel%==0 exit /b 0
                    if %intentos% GEQ 10 exit /b 1
                    ping 127.0.0.1 -n 3 >nul
                    goto loop
                    '''
                }
            }
        }

        stage('Archivar') {
            steps {
                archiveArtifacts artifacts: 'outputs\\**\\*.*', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline completado. Artefactos y logs guardados en Jenkins.'
        }
    }
}