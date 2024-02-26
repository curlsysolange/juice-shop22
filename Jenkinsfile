pipeline {
    agent any
    tools {
        nodejs 'node21'
    }
    
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
        DOCKERHUB_CREDENTIALS = credentials('DockerHubCred')
        SEMGREP_APP_TOKEN = credentials('SEMGREP_APP_TOKEN')
        path_to_host_folder_to_scan = "/mnt/c/Users/bimbi/OneDrive/Desktop/nanadevsec/juice-shop22"
}

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
     stage('Gitleaks Scan') {
            steps {
                script {
                    def gitleaks_report = 'gitleaks.json'
                    sh "gitleaks --report=$path_to_host_folder_to_scan/$gitleaks_report"
                }
            }
        }

        stage('Upload Gitleaks Scan Report to DefectDojo') {
            steps {
                script {
                    uploadScanReport("$path_to_host_folder_to_scan/gitleaks.json")
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=amazonpro -Dsonar.projectKey=amazonpro"
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
            } catch (Exception e) {
                echo "Failed to execute Semgrep scan: ${e.message}"
                currentBuild.result = 'FAILURE'
            }
        }
    }
}

         stage('Upload Semgrep Scan Report to DefectDojo') {
            steps {
                script {
                    uploadScanReport('semgrep.json')
                }
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
        
        stage('Upload Trivy Scan Report to DefectDojo') {
            steps {
                script {
                    uploadScanReport('trivy.json')
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
                        def containername = 'juice-shop22'
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

def uploadScanReport(reportFile) {
    // Upload the scan report to DefectDojo
    // Example command: sh "defectdojo-cli upload --product-name=amazonpro --engagement-name=amazonpro --scan-type=container --file=$reportFile"
}
