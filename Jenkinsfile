pipeline {
	agent { docker { image 'forecast_builder:1.0 } }
	stages {
		stage ('build')
			steps {
				sh 'docker version'
				sh 'docker-compose version'
			}
		}

}
