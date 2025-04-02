pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()  // Wipes old files before checkout
            }
        }

        stage('Force Git Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${env.BRANCH_NAME}"]],
                    extensions: [
                        [$class: 'CleanBeforeCheckout'],  // Prevents stale files
                        [$class: 'LocalBranch'],         // Ensures correct branch
                        [$class: 'CloneOption', depth: 0, noTags: false, shallow: false]
                    ],
                    userRemoteConfigs: [[url: 'YOUR_REPO_URL']]
                ])
                // Verify latest commit
                sh 'git log -1 --pretty=format:"%h - %an, %ar : %s"'
            }
        }

        stage('Build Docker') {
            steps {
                script {
                    echo "Building Docker image for branch: ${env.BRANCH_NAME}"
                    sh """
                        docker build --no-cache --pull -t ${IMAGE_NAME} .
                        echo "----- Dockerfile used -----"
                        cat Dockerfile  // Debug: Verify correct file
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'  // Clean up unused Docker objects
        }
    }
}
