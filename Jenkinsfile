pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDS = credentials('dockerhub-credentials')
        IMAGE_NAME = 'danimm0503/devops-flask-app'
    }

    stages {
        stage('1. Clonar código') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/dperez-a/proyecto-devops-bootcamp.git'
            }
        }

        stage('2. Instalar dependencias') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    pip install pytest pytest-cov flake8
                '''
            }
        }

        stage('3. Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    python -m pytest --cov=app --cov-report=term-missing
                '''
            }
        }

        stage('4. Linting') {
            steps {
                sh '''
                    source venv/bin/activate
                    flake8
                '''
            }
        }

        stage('5. Build imagen Docker') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest -f docker/Dockerfile .'
            }
        }

        stage('6. Push a Docker Hub') {
            when {
                branch pattern: 'main|master|develop', comparator: 'REG_EXP'
            }
            steps {
                sh '''
                    docker login -u ${DOCKER_HUB_CREDS_USR} -p ${DOCKER_HUB_CREDS_PSW} https://index.docker.io/v1/
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -rf venv'
            cleanWs()
        }
        success {
            echo 'Pipeline completado exitosamente'
        }
        failure {
            echo 'Pipeline fallido - revisar logs'
        }
    }
}
