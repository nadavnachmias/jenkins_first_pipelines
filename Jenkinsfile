pipeline {
        agent any
    
        environment {
            // Define the tag variable as an environment variable
            TAG = ''
        }
    
        stages {
            stage('Build') {
                steps {
                    script {
                        // Safely handle the branch name for Docker tag
                        // Make sure BRANCH_NAME is available
                        def branchName = env.BRANCH_NAME ?: "default"  // Default to "default" if BRANCH_NAME is not set
                        TAG = branchName.replaceAll('/', '-').toLowerCase()
    
                        echo "Building Docker image for branch: ${TAG}"
    
                        // Now use the TAG variable in the Docker build command
                        sh """
                            docker build -t myapp:${TAG} .
                        """
                    }
                }
    
        }
    }
}
