pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/app-name"
        DOCKER_CREDENTIALS = "docker-hub-credentials"  // Jenkins credential ID
        CONTAINER_NAME = "flask_test_server"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        stage('Run Server in Docker') {
            steps {
                script {
                    sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def testResult = sh(
                        script: "python3 test-server.py", 
                        returnStatus: true
                    )

                    if (testResult != 0) {
                        error("Tests failed! Stopping pipeline.")
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withDockerRegistry([credentialsId: DOCKER_CREDENTIALS, url: ""]) {
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    sh '''
                    docker stop flask_app || true
                    docker rm flask_app || true
                    docker run -d -p 5000:5000 --name flask_app ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker rm ${CONTAINER_NAME} || true"
        }
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
