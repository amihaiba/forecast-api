pipeline {
    agent {
        label 'build-test'
    }
    stages {
        stage('clean') {
            steps {
                cleanWs()
                sh 'docker stop $(docker ps) && docker rm $(docker ps -a)'
            }
        }
        stage('Fetch git repo') {
            steps {
                git credentialsId: '45551286-fc7b-437b-a6e2-f67305b09ff1', url: 'http://3.88.102.122/gitlab-instance-d4e39dbd/forecast_api'
            }
        }
        stage('Build docker image') {
            steps {
                echo "Workspace: ${env.WORKSPACE}"
                dir(env.WORKSPACE+'/source-files/gunicorn') {
                    sh 'docker build -t forecast_api:latest .'
                }
            }
        }
        stage('Test container') {
            steps {
                dir(env.WORKSPACE+'/source-files') {
                    sh 'docker-compose up -d'
                }
            }
        }
        stage('Push image to Docker hub') {
            steps {
            }
        }
    }
 }
