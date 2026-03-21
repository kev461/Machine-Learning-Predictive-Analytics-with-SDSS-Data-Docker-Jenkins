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

                        echo "Modelos no encontrados. Ejecutando verificación..."

                        bat '''
                        docker run --rm ^
                        -v "%WORKSPACE%:/app" ^
                        -w /app ^
                        python:3.11-slim ^
                        sh -c "pip install -r requirements.txt && PYTHONPATH=/app python run.py --verificar"
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

        stage('Prueba rápida del pipeline') {
            steps {
                bat '''
                docker run --rm ^
                -v "%WORKSPACE%:/app" ^
                -w /app ^
                python:3.11-slim ^
                sh -c "pip install -r requirements.txt && PYTHONPATH=/app python run.py --verificar"
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
                bat '''
                echo Verificando contenedor...
                docker ps

                echo Esperando a que Flask inicie...

                set /a intentos=0

                :loop
                set /a intentos+=1

                curl -f http://localhost:5000/metricas >nul 2>&1
                if %errorlevel%==0 (
                    echo Servidor activo
                    exit /b 0
                )

                if %intentos% GEQ 10 (
                    echo ERROR: servidor no responde
                    docker logs sdss-container
                    exit /b 1
                )

                echo Intento %intentos% fallido, reintentando...
                ping 127.0.0.1 -n 3 >nul
                goto loop
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
            echo 'Pipeline completado. Artefactos guardados en Jenkins.'
        }
    }
}