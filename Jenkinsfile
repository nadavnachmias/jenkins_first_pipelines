pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    // Clean workspace first
                    deleteDir()
                    
                    // Get branch-safe tag name
                    def tag = env.BRANCH_NAME.replaceAll('/', '-').toLowerCase()
                    
                    // Build and tag Docker image
                    sh """
                        docker build -t myapp:${tag} .
                        echo "Successfully built myapp:${tag}"
                    """
                }
            }
        }
    }
}
