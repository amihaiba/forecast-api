pipeline {
    agent {
        label 'build-test'
    }
    stages {
        stage('clean') {
            steps {
                cleanWs()
            }
        }
        stage('git') {
            steps {
                echo 'Fetching git repo'
                git credentialsId: '45551286-fc7b-437b-a6e2-f67305b09ff1', url: 'http://3.88.102.122/gitlab-instance-d4e39dbd/forecast_api'
            }
        }
        stage('build') {
            steps {
                echo 'Building docker image'
                echo "Workspace: ${env.WORKSPACE}"
                dir(env.WORKSPACE+'/source-files/gunicorn') {
                    sh 'docker build -t forecast_api:latest .'
                }
            }
        }       
        stage('test') {
            steps {
                echo 'Testing project'
                dir(env.WORKSPACE+'/source-files') {
                    sh 'docker-compose up -d'
                }
            }
        }
    }
 }
