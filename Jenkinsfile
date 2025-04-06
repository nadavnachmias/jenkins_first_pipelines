pipeline {
    agent any

    environment {
        IMAGE_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        CONTAINER_NAME = "flask-container-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        DOCKER_REPO = "nadavnachmias/flask-app"
        FULL_IMAGE_PATH = "docker.io/${DOCKER_REPO}:${IMAGE_TAG}"
        DEPLOYMENT_NAME = "flask-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        SERVICE_NAME = "svc-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        ROUTE_NAME = "route-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
    }

    stages {

        stage('Build Docker Image') {
            steps {
                script {
                    echo "🔨 Building Docker Image: ${FULL_IMAGE_PATH}"
                    sh "docker build --no-cache -t ${FULL_IMAGE_PATH} ."
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """

                    def findFreePort = {
                        for (int port = 5001; port <= 5100; port++) {
                            def isPortFree = sh(script: "netstat -tuln | grep ':${port} ' || echo 'free'", returnStdout: true).trim()
                            if (isPortFree == "free") {
                                return port
                            }
                        }
                        error("❌ No available ports between 5001–5100")
                    }

                    def port = findFreePort()

                    echo "🚀 Running container on port ${port}"
                    sh """
                        docker run -d \\
                          -p ${port}:5000 \\
                          --name ${CONTAINER_NAME} \\
                          ${FULL_IMAGE_PATH}
                    """

                    env.APP_PORT = port

                    def retries = 10
                    def success = false

                    for (int i = 0; i < retries; i++) {
                        echo "⌛ Waiting for container to start..."
                        sleep 3
                        def status = sh(script: "docker inspect --format='{{.State.Status}}' ${CONTAINER_NAME} || echo 'stopped'", returnStdout: true).trim()
                        if (status == "running") {
                            success = true
                            break
                        }
                    }

                    if (!success) {
                        error("❌ Container did not start in time")
                    }

                    echo "✅ Container is running on port ${env.APP_PORT}"
                }
            }
        }

        stage('Test Run') {
            steps {
                script {
                    echo "🧪 Testing container at http://localhost:${env.APP_PORT}"
                    def testSuccess = sh(
                        script: """
                            for i in {1..3}; do
                                if python3 test-server.py --url http://localhost:${env.APP_PORT}; then
                                    exit 0
                                fi
                                sleep 5
                            done
                            echo "❌ Tests failed after 3 attempts"
                            exit 1
                        """,
                        returnStatus: true
                    )

                    if (testSuccess != 0) {
                        error("❌ Tests failed")
                    }
                    echo "✅ Tests passed successfully!"
                }
            }
        }

        stage('Push to Docker Hub') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    echo "📦 Pushing Docker image: ${FULL_IMAGE_PATH}"
                    withCredentials([usernamePassword(credentialsId: '19b96fb3-0b9e-47c3-8476-e14caf8cd544', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DO_
