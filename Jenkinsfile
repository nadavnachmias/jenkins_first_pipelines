pipeline {
    agent any
    options {
        timeout(time: 10, unit: 'MINUTES')  // Force timeout if stuck
    }
    stages {
        stage('Fast Checkout') {
            steps {
                retry(3) {  // Auto-retry if fails
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${env.BRANCH_NAME}"]],
                        extensions: [
                            [$class: 'CloneOption',
                             depth: 1,  // Only last commit
                             timeout: 2,  // 2-minute timeout
                             shallow: true],
                            [$class: 'CleanBeforeCheckout']
                        ],
                        gitTool: 'Default'
                    ])
                }
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t app:${env.BRANCH_NAME} .'
            }
        }
    }
}
