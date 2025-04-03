pipeline {
    agent any
    
    environment {
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
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
                        
                        // Run the container with dynamic port
                        sh """
                            docker run -d \
                                -p ${TEST_PORT}:5000 \
                                --name flask-test-${IMAGE_TAG} \
                                your-repo/flask-app:${IMAGE_TAG}
                            sleep 5
                        """
                        
                        // Check container logs for Flask startup issues
                        sh "docker logs flask-test-${IMAGE_TAG}"
                        
                        // Ensure Flask is accessible
                        sh """
                            while ! curl --silent --fail http://localhost:${TEST_PORT}; do
                                echo "Waiting for Flask to start..."
                                sleep 5
                            done
                        """
                        
                        // Install test dependencies inside the virtual environment
                        sh """
                            docker exec flask-test-${IMAGE_TAG} /bin/bash -c 'source /app/venv/bin/activate && pip install requests'
                        """
                        
                        // Run tests inside the virtual environment
                        def testExitCode = sh(
                            script: "docker exec flask-test-${IMAGE_TAG} /bin/bash -c 'source /app/venv/bin/activate && python test-server.py --url http://localhost:${TEST_PORT}'",
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

        stage('Deploy to Docker Hub') {
            when {
                branch 'feature-branch' // Only deploy if it's the correct branch (change to your branch name)
            }
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                        """
                    }

                    // Push the image to Docker Hub
                    sh """
                        docker push your-repo/flask-app:${IMAGE_TAG}
                        echo "Pushed image to Docker Hub: your-repo/flask-app:${IMAGE_TAG}"
                    """
                }
            }
        }
    }

    post {
        always {
            // Cleanup unused Docker resources
            sh 'docker system prune -f || true'
        }
    }
}
