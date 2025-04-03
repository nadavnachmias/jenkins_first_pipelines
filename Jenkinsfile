pipeline {
    agent any
    
    stages {
        stage('Setup Python') {
            steps {
                sh '''
                    # Install Python if missing
                    if ! command -v python3 &> /dev/null; then
                        sudo apt-get update
                        sudo apt-get install -y python3 python3-pip
                    fi
                    
                    # Verify installation
                    python3 --version
                    pip3 --version
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    # Install dependencies
                    pip3 install -r requirements.txt
                    
                    # Start server in background
                    python3 server.py &
                    SERVER_PID=$!
                    sleep 5  # Wait for server to start
                    
                    # Run tests
                    python3 test-server.py
                    TEST_RESULT=$?
                    
                    # Stop server
                    kill $SERVER_PID || true
                    
                    # Exit with test status
                    exit $TEST_RESULT
                '''
            }
        }
    }
    
    post {
        always {
            sh '''
                # Cleanup any remaining server processes
                pkill -f "python3 server.py" || true
            '''
        }
    }
}
