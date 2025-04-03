pipeline {
    agent any
    
    environment {
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
        // Get random available port
        HOST_PORT = sh(script: "python -c 'import socket; s=socket.socket(); s.bind((\"\", 0)); print(s.getsockname()[1]); s.close()'", returnStdout: true).trim()
    }
    
    stages {
        stage('Build') {
            steps {
                sh "docker build -t your-repo/flask-app:${IMAGE_TAG} ."
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Run container with dynamic port
                    sh """
                        docker run -d -p ${HOST_PORT}:5000 --name flask-test-${IMAGE_TAG} your-repo/flask-app:${IMAGE_TAG}
                        sleep 5  # Wait for server to start
                        
                        # Test with the dynamically assigned port
                        python3 test_server.py --url http://localhost:${HOST_PORT}
                        
                        # Cleanup
                        docker stop flask-test-${IMAGE_TAG}
                        docker rm flask-test-${IMAGE_TAG}
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh "docker stop flask-test-${IMAGE_TAG} || true"
            sh "docker rm flask-test-${IMAGE_TAG} || true"
        }
    }
}
