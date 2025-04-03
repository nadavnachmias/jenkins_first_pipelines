pipeline {
    agent any
    
    environment {
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    sh """
                        docker build -t your-repo/flask-app:${IMAGE_TAG} .
                    """
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh """
                        docker run -d -p 5000:5000 --name flask-test your-repo/flask-app:${IMAGE_TAG}
                        sleep 10
                        python3 test_server.py
                        docker stop flask-test
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker stop flask-test || true'
            sh 'docker rm flask-test || true'
            sh 'docker system prune -f || true'
        }
    }
}
