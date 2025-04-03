pipeline {
    agent any
    
    environment {
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
        TEST_PORT = "5000" 
    }
    //hello
    stages {
        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t your-repo/flask-app:${IMAGE_TAG} .
                    echo "Successfully built image: your-repo/flask-app:${IMAGE_TAG}"
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    try {
                        // Start container in background
                        sh """
                            docker run -d \
                                -p ${TEST_PORT}:5000 \
                                --name flask-test-${IMAGE_TAG} \
                                your-repo/flask-app:${IMAGE_TAG}
                            sleep 5
                        """
                        
                        // Install test dependencies
                        sh 'pip install requests flask'
                        
                        // Run tests
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
    }
    
    post {
        always {
            sh 'docker system prune -f || true'
        }
    }
}
