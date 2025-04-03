pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}".replaceAll("/", "-").toLowerCase()
        CONTAINER_NAME = "flask-container-${env.BRANCH_NAME}".replaceAll("/", "-").toLowerCase()
        // Get random available port between 5001-5999
        TEST_PORT = sh(script: "shuf -i 5001-5999 -n 1", returnStdout: true).trim()
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image: ${IMAGE_NAME}"
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Run Server Container') {
            steps {
                script {
                    // Cleanup any existing container first
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    
                    echo "Starting Server Container: ${CONTAINER_NAME} on port ${TEST_PORT}"
                    sh """
                        docker run -d \
                            --rm \
                            --name ${CONTAINER_NAME} \
                            -p ${TEST_PORT}:5000 \
                            ${IMAGE_NAME}
                    """
                    sleep 5 // Wait for server to start
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Running Tests against container..."
                    
                    // Install test dependencies in container
                    sh "docker exec ${CONTAINER_NAME} pip install requests"
                    
                    // Run tests and capture exit code
                    def testExitCode = sh(
                        script: "docker exec ${CONTAINER_NAME} python test-server.py --url http://localhost:5000",
                        returnStatus: true
                    )
                    
                    if (testExitCode != 0) {
                        error("❌ Tests failed with exit code ${testExitCode}")
                    } else {
                        echo "✅ All tests passed!"
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    echo "Stopping and Cleaning up..."
                    sh "docker stop ${CONTAINER_NAME} || true"
                    // Keep the image for potential reuse
                }
            }
        }
    }
    
    post {
        always {
            echo "Pipeline completed with status: ${currentBuild.currentResult}"
        }
    }
}
