pipeline {
    agent any

    environment {
        IMAGE_NAME = "my-app"
        ECR_REPO = "992382545251.dkr.ecr.us-east-1.amazonaws.com/yuvaly-repo"
        AWS_REGION = "us-east-1"
        BUILD_TAG = "${BUILD_NUMBER}"                   
        CONTAINER_NAME = "${IMAGE_NAME}-${BRANCH_NAME}-${BUILD_TAG}"
        PORT = "${5000 + BUILD_NUMBER}"                
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_TAG} ."
                }
            }
        }

        stage('Tag for ECR') {
            steps {
                script {
                    sh "docker tag ${IMAGE_NAME}:${BUILD_TAG} ${ECR_REPO}:${BUILD_TAG}"
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin 992382545251.dkr.ecr.${AWS_REGION}.amazonaws.com"
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh "docker push ${ECR_REPO}:${BUILD_TAG}"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker rm -f ${CONTAINER_NAME} || true"

                    sh "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}:${BUILD_TAG}"
                }
            }
        }

        stage('Verify Container') {
            steps {
                script {
                    sh "docker ps | grep ${CONTAINER_NAME}"
                }
            }
        }
    }
}
