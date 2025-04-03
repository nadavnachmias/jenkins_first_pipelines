pipeline {
    agent any
    
    environment {
        // Clean branch name for Docker tag
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
        // Use a fixed port for testing
        TEST_PORT = "5000" 
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t your-repo/flask-app:${IMAGE_TAG} .
                    echo "Successfully built image: your-repo/flask-app:${IMAGE_TAG}"
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    try {
                        // Start container in background
                        sh """
                            docker run -d \
                                -p ${TEST_PORT}:5000 \
                                --name flask-test-${IMAGE_TAG} \
                                your-repo/flask-app:${IMAGE_TAG}
                            sleep 5  # Wait for server to start
                        """
                        
                        // Install test dependencies
                        sh 'pip install requests flask'  # Only dependency needed for testing
                        
                        // Run tests and capture exit code
                        def testExitCode = sh(
                            script: "python test-server.py --url http://localhost:${TEST_PORT}",
                            returnStatus: true
                        )
                        
                        // Fail stage if tests failed
                        if (testExitCode != 0) {
                            error("Tests failed with exit code ${testExitCode}")
                        }
                        
                    } finally {
                        // Always stop and remove container
                        sh """
                            docker stop flask-test-${IMAGE_TAG} || true
                            docker rm flask-test-${IMAGE_TAG} || true
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Cleanup Docker resources
            sh 'docker system prune -f || true'
        }
    }
}
