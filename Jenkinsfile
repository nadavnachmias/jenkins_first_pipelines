pipeline {
    agent any
    
    options {
        timeout(time: 15, unit: 'MINUTES')  // Prevent infinite hangs
        retry(2)  // Auto-retry if checkout fails
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()  // Nuclear option - wipe everything
            }
        }
        
        stage('Fast Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${env.BRANCH_NAME}"]],
                    extensions: [
                        [$class: 'CloneOption',
                         depth: 1,  // Shallow clone (only latest commit)
                         timeout: 5,  // Minutes
                         noTags: true],
                        [$class: 'CleanBeforeCheckout'],
                        [$class: 'LocalBranch']
                    ],
                    doGenerateSubmoduleConfigurations: false,
                    submoduleCfg: []
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Create safe tag name
                    def tag = env.BRANCH_NAME
                        .replaceAll('[^a-zA-Z0-9-]', '-')
                        .toLowerCase()
                    
                    sh """
                        echo "Building Docker image with tag: ${tag}"
                        docker build --no-cache -t myapp:${tag} .
                        docker images | grep myapp:${tag}
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f'  // Clean up Docker
        }
    }
}
