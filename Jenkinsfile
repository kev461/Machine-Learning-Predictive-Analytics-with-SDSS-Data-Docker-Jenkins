pipeline {
    agent any

    environment {
        // Definimos dónde se guardarán los resultados y cómo se llamará nuestro contenedor
        OUTPUTS = "${WORKSPACE}\\outputs"
        IMAGE_NAME = "sdsspipeline"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout') {
            // Buscamos el código más nuevo del proyecto.
            steps {
                // Descargamos el código más reciente desde GitHub
                git branch: 'main', url: 'https://github.com/kev461/Machine-Learning-Predictive-Analytics-with-SDSS-Data-Docker-Jenkins.git'
            }
        }

        stage('Pruebas Dataset') {
            // Se mira si los datos están listos para usarse.
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs

                docker run --rm -v "%WORKSPACE%:/app" %IMAGE_NAME%:%IMAGE_TAG% ^
                python /app/run.py --testdataset ^
                > outputs\\logs\\dataset_test.log 2>&1
                '''
            }
        }

        stage('Verificar modelos') {
            // Si no tenemos un modelo guardado, se entrena.
            steps {
                script {
                    // Si no existen los archivos de los modelos, ejecutamos un proceso para crearlos
                    if (!fileExists('outputs\\modeloClasificacion.pkl') ||
                        !fileExists('outputs\\modeloRegresion.pkl') ||
                        !fileExists('outputs\\modeloClustering.pkl')) {

                        echo "Generando modelos..."
                        bat '''
                        if not exist outputs\\logs mkdir outputs\\logs
                        docker run --rm -v "%WORKSPACE%:/app" -w /app python:3.11-slim ^
                        sh -c "pip install -r requirements.txt && PYTHONPATH=/app python /app/run.py --verificar" ^
                        > outputs\\logs\\verificar_modelos.log 2>&1
                        '''
                    }
                }
            }
        }

        stage('Build Docker') {
            // Ponemos todo en una caja especial (Docker) para que funcione en cualquier lado.
            steps {
                script {
                    // Construimos la imagen de Docker que contiene todo nuestro sistema
                    bat '''
                    if not exist outputs\\logs mkdir outputs\\logs
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% . > outputs\\logs\\docker_build.log 2>&1
                    '''
                }
            }
        }

        stage('Run Docker') {
            //Ponemos a funcionar el programa para que la gente pueda entrar a ver.
            steps {
                script {
                    // Hacemos una llamada rápida al sistema para confirmar que sí está encendido y respondiendo
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
            //Una prueba rápida para asegurar que la máquina prendió bien.
            steps {
                script {
                    // Hacemos una llamada rápida al sistema para confirmar que sí está encendido y respondiendo
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
            // Guardamos todos los resultados y gráficas finales en Jenkins para revisarlos luego
            steps {
                archiveArtifacts artifacts: 'outputs\\**\\*.*', fingerprint: true
            }
        }
    }

    post {
        always {
            // Mensaje final que indica que todo el proceso ha terminado
            echo 'Pipeline completado. Artefactos y logs guardados en Jenkins.'
        }
    }
}