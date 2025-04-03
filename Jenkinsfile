pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                script {
                    sh '''
                        python -m pip install --upgrade pip
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
}
