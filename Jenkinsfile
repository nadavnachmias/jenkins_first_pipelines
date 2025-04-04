pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        CONTAINER_NAME = "flask-container-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
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
                    // Clean up any existing container first
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                    
                    // Find first available port starting from 5001
                    def port = 5001
                    def foundPort = false
                    
                    // Loop to find a free port
                    while (port <= 5100) {
                        def dockerCheck = sh(
                            script: "docker ps --format '{{.Ports}}' | grep -q ':${port}->' && echo 'used' || echo 'free'",
                            returnStdout: true
                        ).trim()

                        def hostCheck = sh(
                            script: "netstat -tuln | grep -q ':${port} ' && echo 'used' || echo 'free'",
                            returnStdout: true
                        ).trim()

                        // Check if the port is free
                        if (dockerCheck == "free" && hostCheck == "free") {
                            foundPort = true
                            break
                        }
                        
                        port++
                    }
                    
                    if (!foundPort) {
                        error("No available ports between 5001-5100")
                    }
                    
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

                    // Simple sleep approach instead of healthcheck
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
                    
                    // Add retries in case of temporary failures
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

                    if (testSuccess != 0) {
                        error("Tests failed after retries")
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
