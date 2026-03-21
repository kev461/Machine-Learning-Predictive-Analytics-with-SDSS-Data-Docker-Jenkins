pipeline {
    agent any

    environment {
        OUTPUTS = "${WORKSPACE}/outputs"
    }

    stages {

        stage('Checkout del repositorio') {
            steps {
                git branch: 'main', url: 'https://github.com/kev461/Machine-Learning-Predictive-Analytics-with-SDSS-Data-Docker-Jenkins.git'
            }
        }

        stage('Instalación de dependencias') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Verificar modelos') {
            steps {
                script {
                    if (!fileExists('outputs/modeloClasificacion.pkl') ||
                        !fileExists('outputs/modeloRegresion.pkl') ||
                        !fileExists('outputs/modeloClustering.pkl')) {
                        echo "Algunos modelos no existen. Se entrenarán automáticamente."
                        bat 'python run.py'
                    } else {
                        echo "Todos los modelos existen. Continuando..."
                    }

                    bat """
                        python -c "import os; \
                        assert os.path.exists('outputs/modeloClasificacion.pkl'); \
                        assert os.path.exists('outputs/modeloRegresion.pkl'); \
                        assert os.path.exists('outputs/modeloClustering.pkl')"
                    """
                }
            }
        }

        stage('Pruebas básicas del dataset') {
            steps {
                bat 'python run.py --test'
            }
        }

        stage('Build Docker') {
            steps {
                echo 'Construyendo imagen Docker...'
                bat 'docker build -t sdsspipeline:latest ./app'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat """
                    docker stop sdss-container || exit 0
                    docker rm sdss-container || exit 0
                    docker run -d --name sdss-container -p 5000:5000 sdsspipeline:latest
                """
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'Verificando que el servicio responde...'
                bat """
                    timeout /t 3
                    curl -f http://localhost:5000/metricas || exit 1
                """
            }
        }

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