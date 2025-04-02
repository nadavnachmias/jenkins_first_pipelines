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
    }
}
