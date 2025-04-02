pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo "Building Docker image for branch: ${env.BRANCH_NAME}"
                    sh """
                        docker build -t ${IMAGE_NAME} .
                    """
                }
            }
        }
    }
}

