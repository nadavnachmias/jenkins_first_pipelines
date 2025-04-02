pipeline {
    agent any
    environment {
        IMAGE_NAME = "flask-app-${env.BRANCH_NAME}"
    }
    stages {
        stage('Clean and Prepare') {
            steps {
                cleanWs()
                // Force fresh clone with full history
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${env.BRANCH_NAME}"]],
                    extensions: [
                        [$class: 'CloneOption',
                         depth: 1,  // Shallow clone (faster)
                         noTags: false,
                         shallow: true,
                         timeout: 10],  // Timeout in minutes
                        [$class: 'CleanBeforeCheckout'],
                        [$class: 'LocalBranch']
                    ],
                    gitTool: 'Default',
                    doGenerateSubmoduleConfigurations: false,
                    submoduleCfg: []
                ])
                sh 'git clean -ffdx'  // Extra cleanup
            }
        }
        
        stage('Verify Files') {
            steps {
                sh '''
                    echo "Current files:"
                    ls -la
                    echo "Dockerfile content:"
                    cat Dockerfile || echo "No Dockerfile found"
                '''
            }
        }

        stage('Build Docker') {
            steps {
                script {
                    try {
                        sh """
                            docker build \
                                --no-cache \
                                --pull \
                                --force-rm \
                                -t ${IMAGE_NAME} .
                        """
                    } catch (e) {
                        error("Docker build failed: ${e}")
                    }
                }
            }
        }
    }
    post {
        always {
            sh 'docker system prune -f --all'
        }
    }
}
