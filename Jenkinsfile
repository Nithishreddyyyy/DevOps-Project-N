pipeline {
    agent any

    environment {

        FRONTEND_IMAGE = "nithishreddyyy/devops-frontend"
        BACKEND_IMAGE = "nithishreddyyy/devops-backend"

        DOCKER_CREDS = credentials('dockerhub-creds')
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/Nithishreddyyyy/DevOps-Project-N.git'
            }
        }

        stage('Frontend Dependency Install') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                }
            }
        }

        stage('Backend Dependency Install') {
            steps {
                dir('backend') {
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                sh '''
                sonar-scanner \
                  -Dsonar.token=$SONAR_TOKEN
                '''
            }
        }

        stage('Trivy Filesystem Scan') {
            steps {
                sh '''
                trivy fs . \
                --severity HIGH,CRITICAL \
                --exit-code 0
                '''
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                dir('frontend') {
                    sh 'docker build -t $FRONTEND_IMAGE:latest .'
                }
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                dir('backend') {
                    sh 'docker build -t $BACKEND_IMAGE:latest .'
                }
            }
        }

        stage('Docker Hub Login') {
            steps {
                sh '''
                echo $DOCKER_CREDS_PSW | docker login \
                -u $DOCKER_CREDS_USR \
                --password-stdin
                '''
            }
        }

        stage('Push Frontend Docker Image') {
            steps {
                sh 'docker push $FRONTEND_IMAGE:latest'
            }
        }

        stage('Push Backend Docker Image') {
            steps {
                sh 'docker push $BACKEND_IMAGE:latest'
            }
        }

        stage('Deployment') {
            steps {
                echo 'Deployment handled through Vercel and Render auto deployment'
            }
        }

        stage('Dep') {
            steps {
                sh 'vercel --prod .'
            }
        }
    }

    post {

        success {
            echo 'CI/CD Pipeline executed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed!'
        }

        always {
            sh 'docker logout'
        }
    }
}
