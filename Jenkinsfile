pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        CONTAINER_NAME = "flask-container-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        DOCKER_REGISTRY = "docker.io"  // Use docker.io (Docker Hub) or your custom registry
        DOCKER_REPO = "nadavnachmias/flask-app"  // Your Docker Hub repository
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

        stage('Run Container') {
            steps {
                script {
                    // Clean up any existing container first!
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                    
                    // Function to find the first available port between 5001 and 5100
                    def findFreePort = { 
                        for (int port = 5001; port <= 5100; port++) {
                            def isPortFree = sh(script: "netstat -tuln | grep -q ':${port} ' || echo 'free'", returnStdout: true).trim()
                            if (isPortFree == "free") {
                                return port
                            }
                        }
                        error("No available ports between 5001-5100")
                    }

                    def port = findFreePort()

                    echo "Starting container on port ${port} (container port 5000)"
                    sh """
                        docker run -d \\
                          -p ${port}:5000 \\
                          --name ${CONTAINER_NAME} \\
                          ${IMAGE_NAME}
                    """
                    
                    env.APP_PORT = port

                    // Wait for container to be healthy
                    def retries = 10
                    def success = false

                    for (int i = 0; i < retries; i++) {
                        echo "Waiting for the container to start..."
                        sleep 3
                        
                        def containerStatus = sh(
                            script: "docker inspect --format='{{.State.Status}}' ${CONTAINER_NAME} || echo 'stopped'",
                            returnStdout: true
                        ).trim()

                        if (containerStatus == "running") {
                            echo "Container is running"
                            success = true
                            break
                        }
                    }

                    if (!success) {
                        error("Container did not start in time")
                    }

                    echo "Application running on host port ${port} (container port 5000)"
                }
            }
        }

        stage('test-run') {
            steps {
                script {
                    echo "Testing on port ${env.APP_PORT}"
                    
                    // Run the tests with retries in case of failure
                    def testSuccess = sh(
                        script: """
                            for i in {1..3}; do
                                if python3 test-server.py --url http://localhost:${env.APP_PORT}; then
                                    exit 0
                                fi
                                sleep 5
                            done
                            echo "Tests failed after 3 attempts"
                            exit 1
                        """,
                        returnStatus: true
                    )

                    // If the tests fail, abort the pipeline by using the 'error' step
                    if (testSuccess != 0) {
                        error("Tests failed after retries")  // This will stop the pipeline with an error
                    }
                    echo "Tests passed successfully!"  // If tests pass, proceed
                }
            }
        }

        stage('Push to Docker Hub') {
            when {
                // Only push to Docker Hub if the tests passed
                expression { return currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    echo "Pushing Docker image ${DOCKER_REPO}:${env.BRANCH_NAME}"

                    // Login to Docker Hub using the credentials ID
                    withCredentials([usernamePassword(credentialsId: '19b96fb3-0b9e-47c3-8476-e14caf8cd544', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh """
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin
                        """
                    }
                    
                    // Tag the image with the Docker Hub repository name
                    sh """
                        docker tag ${IMAGE_NAME} ${DOCKER_REGISTRY}/${DOCKER_REPO}:${env.BRANCH_NAME}
                    """
                    
                    // Push the image to Docker Hub
                    sh """
                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}:${env.BRANCH_NAME}
                    """
                }
            }
        }
    }

    post {
        always {
            // Cleanup the workspace after the build
            cleanWs()
        }
    }
}
