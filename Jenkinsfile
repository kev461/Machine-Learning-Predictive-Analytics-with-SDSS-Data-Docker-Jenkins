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

        stage('Verificar modelos') {
            steps {
                script {
                    if (!fileExists('outputs\\modeloClasificacion.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloClustering.pkl')) {

                        echo "Generando modelos..."

                        bat '''
                        docker run --rm ^
                        -v "%WORKSPACE%:/app" ^
                        -w /app ^
                        python:3.11-slim ^
                        sh -c "pip install -r requirements.txt && PYTHONPATH=/app python /app/run.py --verificar"
                        '''
                    }
                }
            }
        }

        stage('Build Docker') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Run Docker') {
            steps {
                bat '''
                docker stop sdss-container 2>nul
                docker rm sdss-container 2>nul

                docker run -d ^
                --name sdss-container ^
                -v "%WORKSPACE%\\outputs:/app/outputs" ^
                -p 5000:5000 ^
                %IMAGE_NAME%:%IMAGE_TAG%
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                bat '''
                set /a intentos=0

                :loop
                set /a intentos+=1

                curl -f http://localhost:5000/metricas >nul 2>&1
                if %errorlevel%==0 exit /b 0

                if %intentos% GEQ 10 exit /b 1

                ping 127.0.0.1 -n 3 >nul
                goto loop
                '''
            }
        }

        stage('Archivar') {
            steps {
                archiveArtifacts artifacts: 'outputs\\**\\*.*', fingerprint: true
            }
        }
    }
}