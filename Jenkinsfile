pipeline {
    agent {
        label 'build-test'
    }
    stages {
        stage('clean') {
            cleanWs()
        }
        stage('git') {
            steps {
                echo 'Fetching git repo'
                git credentialsId: '45551286-fc7b-437b-a6e2-f67305b09ff1', url: 'http://3.88.102.122/gitlab-instance-d4e39dbd/forecast_api'
            }
        }
        stage('build') {
            steps {
                echo 'Building project'
            }
        }       
        stage('test') {
            steps {
                echo 'Testing project'
            }
        }
    }
 }
