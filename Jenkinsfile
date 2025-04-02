pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    // Safely handle branch name for Docker tag
                    def tag = env.BRANCH_NAME.replaceAll('/', '-').toLowerCase()

                    sh """
                        echo "Building Docker image for branch: ${tag}"
                        docker build -t myapp:${tag} .
                    """
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run pytest tests inside the container
                    echo "Running pytest tests"
                    
                    // Assuming you have the test suite inside the Docker image or have mounted the tests from the host
                    sh """
                        docker run --rm myapp:${tag} pytest > result.log; tail -n 10 result.log
                    """
                }
            }
        }
    }
}
