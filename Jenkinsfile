pipeline {
    agent any
    tools {
        nodejs 'node21'
    }
    
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
        DOCKERHUB_CREDENTIALS = credentials('DockerHubCred')
        SEMGREP_APP_TOKEN = credentials('SEMGREP_APP_TOKEN')
    }
    
    stages {
        stage('Clean workspace') {
            steps {
                cleanWs()
            }
        }
        
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Abbyabiola/juice-shop22.git'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=amazonpro -Dsonar.projectKey=amazonpro"
                }
            }
        }
        
        stage('NPM Install') {
            steps {
                sh 'npm install'
            }
        }
        
        stage('Trivy File Scan') {
            steps {
                script {
                    sh 'trivy fs . > trivy_result.txt'  // Assuming Trivy is properly installed
                }
            }
        }
    
        stage('Login to DockerHUB') {
            steps {
                script {
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    echo 'Login Succeeded'
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    sh 'docker build -t abimbola1981/juice-shop22:latest .' 
                    echo "Image Build Successfully"
                }
            }
        }
        
        stage('Semgrep-Scan') {
            steps {
                script {
                    try {
                        // Pull the Semgrep Docker image
                        sh 'docker pull returntocorp/semgrep'
                        
                        // Run Semgrep scan within the Docker container
                        sh '''
                            docker run \
                            -e SEMGREP_APP_TOKEN=$SEMGREP_APP_TOKEN \
                            -v "$(pwd):/workspace" \
                            -w "/workspace" \
                            returntocorp/semgrep semgrep ci
                        '''
                    } catch (Exception e) {
                        echo "Failed to execute Semgrep scan: ${e.message}"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage('Trivy Image Scan') {
            steps {
                script {
                    try {
                        sh 'trivy image abimbola1981/juice-shop22:latest'
                        sh 'pwd'
                    } catch (Exception e) {
                        echo "Failed to execute Trivy image scan: ${e.message}"
                    }
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    sh 'docker push abimbola1981/juice-shop22:latest'
                    echo "Push Image to Registry"
                }
            }
        }
        
        stage('Containerization Deployment') {
            steps {
                script {
                    try {
                        def containername = 'amazonproject'
                        def isRunning = sh(script: "docker ps -a | grep ${containername}", returnStatus: true)
                        if (isRunning == 0) {
                            sh "docker stop ${containername}"
                            sh "docker rm ${containername}"
                        }
                        sh "docker run -d -p 3000:3000 --name ${containername} abimbola1981/juice-shop22:latest"
                    } catch (Exception e) {
                        echo "Failed to deploy container: ${e.message}"
                    }
                }
            }
        }
    }
}
