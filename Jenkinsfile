pipeline {
    agent {
        label 'build-test'
    }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
    }
    stages {
        stage('clean') {
            steps {
                cleanWs()
                sh 'if [[ -n $(docker ps -q) ]]; then docker stop $(docker ps -q) fi'
                sh 'docker rm $(docker ps -aq) && docker image prune -f'
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
                    sh "docker build -t amihaiba/forecast_api:${env.BUILD_NUMBER} ."
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
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh "docker push amihaiba/forecast_api:${env.BUILD_NUMBER}"
                echo 'Shtrudel'
            }
        }
    }
    post {
        success {
            slackSend channel: "#succeeded-built", color: "good", message: "Build ${env.JOB_NAME} ${env.BUILD_NUMBER} finished successfuly!"
        }
        failure {
            slackSend channel: "#succeeded-built", color: "warning", message: "Build ${env.JOB_NAME} ${env.BUILD_NUMBER} failed!"
        }
    }
 }
