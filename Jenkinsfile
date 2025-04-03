pipeline {
    agent any
    
    environment {
        // Clean branch name for Docker tag
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
        // Get random available port
        TEST_PORT = sh(script: "shuf -i 5001-5999 -n 1", returnStdout: true).trim()
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
        
        stage('Run Tests') {
            steps {
                script {
                    try {
                        // Clean up any previous container
                        sh "docker stop flask-test-${IMAGE_TAG} || true"
                        sh "docker rm flask-test-${IMAGE_TAG} || true"
                        
                        // Run container with dynamic port
                        sh """
                            docker run -d \
                                -p ${TEST_PORT}:5000 \
                                --name flask-test-${IMAGE_TAG} \
                                your-repo/flask-app:${IMAGE_TAG}
                            sleep 5
                        """
                        
                        // Install test dependencies
                        sh 'pip install requests'
                        
                        // Run tests
                        def testExitCode = sh(
                            script: "python test-server.py --url http://localhost:${TEST_PORT}",
                            returnStatus: true
                        )
                        
                        if (testExitCode != 0) {
                            error("Tests failed with exit code ${testExitCode}")
                        }
                        
                    } finally {
                        // Cleanup container
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
            sh 'docker system prune -f || true'
        }
    }
}
