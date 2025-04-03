pipeline {
    agent any
    
    environment {
        // Clean branch name for Docker tag
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t your-repo/flask-app:${IMAGE_TAG} .
                    echo "Built image: your-repo/flask-app:${IMAGE_TAG}"
                """
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Install test dependencies
                    sh 'pip install -r requirements.txt'
                    
                    try {
                        // Start server in background
                        sh 'python server.py &'
                        sleep(time: 5, unit: 'SECONDS')
                        
                        // Run tests
                        def testResult = sh(
                            script: 'python test-server.py',
                            returnStatus: true
                        )
                        
                        if (testResult != 0) {
                            error("Tests failed with exit code ${testResult}")
                        }
                    } finally {
                        // Stop server (works even if tests fail)
                        sh 'pkill -f "python server.py" || true'
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up Docker and any remaining processes
            sh 'docker system prune -f || true'
            sh 'pkill -f "python server.py" || true'
        }
    }
}
