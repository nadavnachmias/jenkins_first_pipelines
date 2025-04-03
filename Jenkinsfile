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
                        sh "docker stop flask-test-${IMAGE_TAG} || true"
                        sh "docker rm flask-test-${IMAGE_TAG} || true"
                        
                        sh """
                            docker run -d \
                                -p ${TEST_PORT}:5000 \
                                --name flask-test-${IMAGE_TAG} \
                                your-repo/flask-app:${IMAGE_TAG}
                            sleep 5
                        """
                        
                        sh 'pip install requests'
                        
                        def testExitCode = sh(
                            script: "python test-server.py --url http://localhost:${TEST_PORT}",
                            returnStatus: true
                        )
                        
                        if (testExitCode != 0) {
                            error("Tests failed with exit code ${testExitCode}")
                        }
                        
                    } finally {
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
            sh 'docker system prune -f || true'
        }
    }
}
