pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    def imageTag = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
                    sh """
                        docker build -t your-repo/flask-app:${imageTag} .
                    """
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    def imageTag = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
                    sh """
                        docker run -d -p 5000:5000 --name flask-test your-repo/flask-app:${imageTag}
                        sleep 5
                        python3 test_server.py || exit 1
                        docker stop flask-test
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f'
        }
    }
}
