pipeline {
    agent any
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Use the branch name as the image tag
                    def imageTag = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
                    
                    sh """
                        echo "Building Docker image with tag: ${imageTag}"
                        docker build -t your-repo/flask-app:${imageTag} .
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f'  // Clean up unused containers
        }
    }
}
