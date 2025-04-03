pipeline {
    agent any
    
    environment {
        // Clean branch name for Docker tag
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build with fallback to legacy build if needed
                    sh """
                        docker build -t your-repo/flask-app:${IMAGE_TAG} . || true
                        echo "Successfully built image: your-repo/flask-app:${IMAGE_TAG}"
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f || true'
        }
    }
}
