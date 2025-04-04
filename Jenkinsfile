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
                    
                    while(port <= 5100) {
                        // Check if port is in use by any container
                        def dockerCheck = sh(
                            script: "docker ps --format '{{.Ports}}' | grep -c ':${port}->' || true",
                            returnStdout: true
                        ).trim().toInteger()
                        
                        // Check if port is in use on host system
                        def hostCheck = sh(
                            script: "netstat -tuln | grep -c ':${port} ' || true",
                            returnStdout: true
                        ).trim().toInteger()
                        
                        if (dockerCheck == 0 && hostCheck == 0) {
                            foundPort = true
                            break
                        }
                        
                        port++
                    }
                    
                    if (!foundPort) {
                        error("No available ports between 5001-5100")
                    }
                    
                    // Run container with the found port
                    echo "Starting container on port ${port} (container port 5000)"
                    sh """
                        docker run -d \\
                          -p ${port}:5000 \\
                          --name ${CONTAINER_NAME} \\
                          ${IMAGE_NAME}
                    """
                    
                    env.APP_PORT = port
            
                    // Wait for container to be healthy
                    sh """
                        for i in {1..10}; do
                            if docker inspect --format='{{.State.Health.Status}}' ${CONTAINER_NAME} | grep -q healthy; then
                                echo "Container ready"
                                break
                            fi
                            sleep 3
                        done
                    """
                    
                    echo "Application running on host port ${port} (container port 5000)"
                }
            }
        }
        
        stage ('test-run') {
            steps {
                script {
                    echo "Testing on port ${env.APP_PORT}"
                    
                    // Add retries in case of temporary failures
                    sh """
                        for i in {1..3}; do
                            if python3 test-server.py --url http://localhost:${env.APP_PORT}; then
                                exit 0
                            fi
                            sleep 5
                        done
                        echo "Tests failed after 3 attempts"
                        exit 1
                    """
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
