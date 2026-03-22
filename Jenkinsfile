pipeline {
    agent any

    environment {
        OUTPUTS = "${WORKSPACE}\\outputs"
        IMAGE_NAME = "sdsspipeline"
        IMAGE_TAG = "latest"
    }

    // Función interna para ejecutar comandos y guardar logs
    def runWithLog = { cmd, logName ->
        bat """
        if not exist outputs\\logs mkdir outputs\\logs
        ${cmd} > outputs\\logs\\${logName}.log 2>&1
        """
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kev461/Machine-Learning-Predictive-Analytics-with-SDSS-Data-Docker-Jenkins.git'
            }
        }

        stage('Verificar modelos') {
            steps {
                script {
                    if (!fileExists('outputs\\modeloClasificacion.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloClustering.pkl')) {

                        echo "Generando modelos..."
                        runWithLog(
                            'docker run --rm -v "%WORKSPACE%:/app" -w /app python:3.11-slim sh -c "pip install -r requirements.txt && PYTHONPATH=/app python /app/run.py --verificar"',
                            'verificar_modelos'
                        )
                    }
                }
            }
        }

        stage('Build Docker') {
            steps {
                script {
                    runWithLog('docker build -t %IMAGE_NAME%:%IMAGE_TAG% .', 'docker_build')
                }
            }
        }

        stage('Run Docker') {
            steps {
                script {
                    runWithLog('docker stop sdss-container 2>nul & docker rm sdss-container 2>nul & docker run -d --name sdss-container -v "%WORKSPACE%\\outputs:/app/outputs" -p 5000:5000 %IMAGE_NAME%:%IMAGE_TAG%', 'docker_run')
                }
            }
        }

        stage('Smoke Test') {
            steps {
                script {
                    // Loop de intentos
                    def maxIntentos = 10
                    def logFile = "${WORKSPACE}\\outputs\\logs\\smoke_test.log"
                    bat """
                    if not exist outputs\\logs mkdir outputs\\logs
                    set /a intentos=0
                    :loop
                    set /a intentos+=1
                    curl -f http://localhost:5000/metricas > ${logFile} 2>&1
                    if %errorlevel%==0 exit /b 0
                    if %intentos% GEQ ${maxIntentos} exit /b 1
                    ping 127.0.0.1 -n 3 >nul
                    goto loop
                    """
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