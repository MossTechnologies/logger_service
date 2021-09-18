properties([disableConcurrentBuilds()])

pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
        timestamps()
    }

    environment {
        def BUILD_VERSION = sh(script: "echo `date +'%Y%m%d-%H%M'`", returnStdout: true).trim()
        def DOCKER_IMAGE_NAME = "wunu_logger_service"
        def PRE_TEXT = """*${env.BUILD_TAG}*\n\n*Build:* ${env.BUILD_ID}\n*Build Version:* ${BUILD_VERSION}\n\n<https://smart.wunu.edu.ua/serviceJenkins/job/${env.JOB_NAME}/${env.BUILD_ID}/console|View console output>\n\n"""
    }

    stages {
        stage("Notify about start of work") {
            steps {
                slackSend channel: 'jenkins', color: "#1390d4", message: "${env.PRE_TEXT} Build Started :rocket:"
            }
        }
        stage("Create Docker image") {
            steps {
                echo "=== Start building docker image ==="
                sh 'docker stop wunu_logger_service || true'
                sh 'docker rm wunu_logger_service || true'
                sh 'docker rmi wunu_logger_service || true'
                sh """docker build --shm-size 1G -t ${DOCKER_IMAGE_NAME}:latest . """
            }
        }
        stage("Start docker image") {
            steps {
                echo "=== Start docker image ==="

                sh """docker run -d --net=host --restart=always --name wunu_logger_service ${DOCKER_IMAGE_NAME}:latest"""
            }
        }
    }

    post {
        always {
            echo 'One way or another, I have finished'
            deleteDir() /* clean up our workspace */
        }
        success {
            slackSend channel: 'jenkins', color: "#35b035", message: "${env.PRE_TEXT} Build Success :white_check_mark:"
        }
        unstable {
            slackSend channel: 'jenkins', color: "#d41326", message: "${env.PRE_TEXT} Build Unstable :no_entry:"
        }
        failure {
            slackSend channel: 'jenkins', color: "#d41326", message: "${env.PRE_TEXT} Build Failure :no_entry:"
        }
        changed {
            echo 'Things were different before...'
        }
    }
}