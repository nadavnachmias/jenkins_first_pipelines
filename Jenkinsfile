pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        CONTAINER_NAME = "flask-container-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        DOCKER_REGISTRY = "docker.io"
        DOCKER_REPO = "nadavnachmias/flask-app"
        FULL_IMAGE_PATH = "docker.io/nadavnachmias/flask-app:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        DEPLOYMENT_NAME = "flask-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        SERVICE_NAME = "svc-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()
        ROUTE_NAME = "route-${env.BRANCH_NAME}".replaceAll("[^a-zA-Z0-9-]", "-").toLowerCase()

    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image: ${IMAGE_NAME}"
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
                            echo "Checking port ${port}: ${isPortFree}"
                            if (isPortFree == "free") {
                                return port
                            }
                        }
                        error("No available ports between 5001-5100")
                    }

                    def port = findFreePort()

                    echo "Starting containerr on port ${port} (container port 5000)"
                    sh """
                        docker run -d \\
                          -p ${port}:5000 \\
                          --name ${CONTAINER_NAME} \\
                          ${IMAGE_NAME}
                    """
                    
                    env.APP_PORT = port

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
                    echo "Tests passed successfully!"
                }
            }
        }

        stage('Push to Docker Hub') {
            when {
                expression { return currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    echo "Pushing Docker image ${DOCKER_REPO}:${env.BRANCH_NAME}"

                    withCredentials([usernamePassword(credentialsId: '19b96fb3-0b9e-47c3-8476-e14caf8cd544', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh """
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin
                        """
                    }
                    
                    sh """
                        docker tag ${IMAGE_NAME} ${FULL_IMAGE_PATH}
                        docker push ${FULL_IMAGE_PATH}
                    """
                }
            }
        }

        stage('Deploy to OpenShift') {
            steps {
                script {
                        sh """
                        echo 'Logging into OpenShift...'
                        oc login --token=sha256~74v_zFctW2ZmN9DDl1tCG44ns65lGt-9XjRqGD3zSY8 --server=https://api.rm1.0a51.p1.openshiftapps.com:6443
        
                        echo 'Switching to project...'
                        oc project nadav2341-dev
        
                        echo 'Checking if deployment ${DEPLOYMENT_NAME} exists...'
                        if ! oc get deployment/${DEPLOYMENT_NAME}; then
                          echo 'Creating deployment ${DEPLOYMENT_NAME}...'
                          oc create deployment ${DEPLOYMENT_NAME} --image=${FULL_IMAGE_PATH} --port=5000
                          oc expose deployment ${DEPLOYMENT_NAME} --port=5000 --name=${SERVICE_NAME}
                          oc expose svc/${SERVICE_NAME} --name=${ROUTE_NAME}
                        else
                          echo 'Deployment exists. Updating image...'
                          oc set image deployment/${DEPLOYMENT_NAME} flask-app=${FULL_IMAGE_PATH}
                          oc rollout restart deployment/${DEPLOYMENT_NAME}
                        fi
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
