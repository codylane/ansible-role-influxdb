pipeline {

    agent any

    stages {

        stage ('Prep') {
            steps {
                ansiColor('xterm') {
                    sh """
#!/bin/bash -e

cd codylane.influxdb
.travis/init
"""
                }
            }
        }

        stage ('Build') {
            steps {
                ansiColor('xterm') {
                    sh """
#!/bin/bash -e

cd codylane.influxdb
. .venv/bin/activate
invoke travis
"""
                }

            }
        }
    }

}
