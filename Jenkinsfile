pipeline {
    agent any

    environment {
        // Credenciales seguras inyectadas desde Jenkins con prefijos únicos
        HEART_MONGO_URI = credentials('HEART_MONGO_URI')
        HEART_MONGO_DB = credentials('HEART_MONGO_DB')
        HEART_MONGO_COLECCION = credentials('HEART_MONGO_COLECCION')
        HEART_NGROK_TOKEN = credentials('HEART_NGROK_TOKEN')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kev461/HearthDiseaseStream.git'
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // Creamos el directorio de logs de forma segura
                    bat 'if not exist outputs\\logs mkdir outputs\\logs'
                    
                    // Limpiamos posibles espacios o saltos de línea de las credenciales de Jenkins
                    def mongoUri = env.HEART_MONGO_URI.trim()
                    def mongoDb = env.HEART_MONGO_DB.trim()
                    def mongoColl = env.HEART_MONGO_COLECCION.trim()
                    def ngrokToken = env.HEART_NGROK_TOKEN.trim()
                    
                    // Usamos writeFile para evitar problemas con caracteres especiales
                    def envContent = """
HEART_MONGO_URI=${mongoUri}
HEART_MONGO_DB=${mongoDb}
HEART_MONGO_COLECCION=${mongoColl}
HEART_NGROK_TOKEN=${ngrokToken}
""".trim()
                    writeFile file: '.env', text: envContent
                    echo "Archivo .env creado con prefijos HEART_ exitosamente."
                }
            }
        }

        stage('Build Image') {
            steps {
                // Construimos la imagen base una sola vez para usarla en pruebas y despliegue
                bat 'docker build -t heart-disease-app .'
            }
        }

        stage('Pruebas Dataset') {
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs
                docker run --rm -v "%WORKSPACE%:/app" heart-disease-app ^
                python /app/modulos_datos/verificar_dataframe.py ^
                > outputs\\logs\\heart_dataset_test.log 2>&1
                '''
            }
        }

        stage('Prueba Mongo') {
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs
                docker run --rm ^
                -e HEART_MONGO_URI="%HEART_MONGO_URI%" ^
                -e HEART_MONGO_DB="%HEART_MONGO_DB%" ^
                -e HEART_MONGO_COLECCION="%HEART_MONGO_COLECCION%" ^
                heart-disease-app ^
                python /app/flujos/test_mongo.py ^
                > outputs\\logs\\heart_mongo_test.log 2>&1
                '''
            }
        }

        stage('Deploy Infrastructure') {
            steps {
                bat '''
                if not exist outputs\\logs mkdir outputs\\logs
                docker-compose down --remove-orphans
                docker-compose up -d --build --force-recreate > outputs\\logs\\docker_compose_up.log 2>&1
                '''
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
                    curl -f http://localhost:5000/stats > outputs\\logs\\smoke_test.log 2>&1
                    if %errorlevel%==0 exit /b 0
                    if %intentos% GEQ 15 exit /b 1
                    ping 127.0.0.1 -n 4 >nul
                    goto loop
                    '''
                }
            }
        }

        stage('Exponer URL') {
            steps {
                echo "--- REVISANDO ESTADO DE NGROK ---"
                // Esperamos un poco a que ngrok intente conectar
                bat 'ping 127.0.0.1 -n 5 >nul'
                bat 'docker logs ngrok'
                echo "--- API DE TÚNELES (JSON) ---"
                bat 'curl -s http://localhost:4040/api/tunnels'
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
            echo 'Pipeline completado. Revisar logs en los artefactos de Jenkins.'
        }
    }
}
