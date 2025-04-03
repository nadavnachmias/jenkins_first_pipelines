pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}".replaceAll("/", "-").toLowerCase()
        CONTAINER_NAME = "flask-container-${env.BRANCH_NAME}".replaceAll("/", "-").toLowerCase()
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
                    echo "Starting Server Container: ${CONTAINER_NAME}"
                    sh "docker run -d --rm --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}"
                    sleep 5 // Wait for the server to start
                }
            }
        }

        stage('Run Tests') {
    steps {
        script {
            echo "Running Test Script inside the container..."
            def testExitCode = sh(script: "docker exec ${CONTAINER_NAME} python test-server.py", returnStatus: true)

            if (testExitCode == 0) {
                echo "Tests Passed ✅"
            } else {
                error("Tests Failed ❌")
            }
        }
    }
}


        stage('Cleanup') {
            steps {
                script {
                    echo "Stopping and Cleaning up..."
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rmi ${IMAGE_NAME} || true"
                }
            }
        }
    }
    
    post {
        success {
            echo "Pipeline completed successfully 🚀"
        }
        failure {
            echo "Pipeline failed ❌"
        }
    }
}
