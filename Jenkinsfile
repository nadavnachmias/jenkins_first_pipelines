pipeline {
    agent any

    environment {
        // Sanitize branch name for use in image/container names
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
                    // Find available port starting from 5000
                    def port = 5000
                    while(true) {
                        def occupied = sh(
                            script: "docker ps --format '{{.Ports}}' | grep ':${port}->' || true",
                            returnStatus: true
                        )
                        if (occupied != 0) break
                        port++
                        if (port > 5100) error("No available ports")
                    }
                    
                    sh """
                        docker run -d \
                          -p ${port}:${port} \
                          -e PORT=${port} \
                          --name ${CONTAINER_NAME} \
                          ${IMAGE_NAME}
                    """
                    echo "Application running on port ${port}"
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
