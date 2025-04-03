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



stage('Test') {
    steps {
        script {
            def imageTag = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
            sh """
                docker run -d -p 5000:5000 --name flask-test your-repo/flask-app:${imageTag}
                sleep 5
                python3 test-server.py || exit 1  # Fail pipeline if tests fail
                docker stop flask-test
            """
        }
    }
}	    
    post {
        always {
            sh 'docker system prune -f'  // Clean up unused containers
        }
    }
}
