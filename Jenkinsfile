pipeline {
    agent any

    environment {
        OUTPUTS = "${WORKSPACE}/outputs"
    }

    stages {

        // Checkout del repositorio
        stage('Checkout del repositorio') {
            steps {
                git branch: 'main', url: 'https://github.com/kev461/Machine-Learning-Predictive-Analytics-with-SDSS-Data-Docker-Jenkins.git'
            }
        }

        // 2️⃣ Instalación de dependencias
        stage('Instalación de dependencias') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        // Verificar modelos
        stage('Verificar modelos') {
            steps {
                script {
                    if (!fileExists('outputs/modeloClasificacion.pkl') ||
                        !fileExists('outputs/modeloRegresion.pkl') ||
                        !fileExists('outputs/modeloClustering.pkl')) {
                        echo "Algunos modelos no existen. Se entrenarán automáticamente."
                        sh 'python run.py'
                    } else {
                        echo "Todos los modelos existen. Continuando..."
                    }

                    // Asegurarse que los modelos existen
                    sh "python -c \"import os; assert os.path.exists('outputs/modeloClasificacion.pkl'); assert os.path.exists('outputs/modeloRegresion.pkl'); assert os.path.exists('outputs/modeloClustering.pkl')\""
                }
            }
        }

        // Pruebas básicas del dataset
        stage('Pruebas básicas del dataset') {
            steps {
                sh 'python run.py --test'
            }
        }

        // Construcción de la imagen Docker
        stage('Build Docker') {
            steps {
                echo 'Construyendo imagen Docker...'
                sh 'docker build -t sdsspipeline:latest ./app'
            }
        }

        // Ejecutar contenedor Docker
        stage('Run Docker Container') {
            steps {
                sh '''
                    docker stop sdss-container || true
                    docker rm sdss-container || true
                    docker run -d --name sdss-container -p 5000:5000 sdsspipeline:latest
                '''
            }
        }

        // Smoke test
        stage('Smoke Test') {
            steps {
                echo 'Verificando que el servicio responde...'
                sh '''
                    sleep 3
                    curl -f http://localhost:5000/metricas || exit 1
                '''
            }
        }

        // Guardar artefactos
        stage('Almacenamiento de artefactos') {
            steps {
                archiveArtifacts artifacts: 'outputs/**/*.*', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline completado. Artefactos guardados en Jenkins.'
        }
    }
}