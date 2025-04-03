pipeline {
    agent any
    
    environment {
        IMAGE_TAG = "${env.BRANCH_NAME.toLowerCase().replaceAll('[^a-z0-9-]', '-')}"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Check if buildx is available, fall back to legacy build if not
                    def buildCommand = """
                        if docker buildx version >/dev/null 2>&1; then
                            docker buildx build -t your-repo/flask-app:${IMAGE_TAG} .
                        else
                            echo "Buildx not available, using legacy build"
                            docker build -t your-repo/flask-app:${IMAGE_TAG} .
                        fi
                    """
                    sh buildCommand
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh '''
                        pip install -r requirements.txt
                        python server.py &
                        sleep 5
                        python test-server.py || exit 1
                        pkill -f "python server.py" || true
                    '''
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f || true'
            sh 'pkill -f "python server.py" || true'
        }
    }
}
