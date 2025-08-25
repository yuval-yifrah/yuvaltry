pipeline {
    agent any

    environment {
        IMAGE_NAME = "my-app"
        ECR_REPO = "992382545251.dkr.ecr.us-east-1.amazonaws.com/yuvaly"
        AWS_REGION = "us-east-1"
        BUILD_TAG = "candidate-${BUILD_NUMBER}"
        CONTAINER_NAME = "${IMAGE_NAME}-prod"
        PROD_HOST = "ec2-user@52.87.183.251"
        PROD_PORT = "5000"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_TAG} ."
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    
                    sh "docker run --rm ${IMAGE_NAME}:${BUILD_TAG} pytest || exit 1"
                }
            }
        }

        stage('Tag for ECR') {
            steps {
                script {
                    sh "docker tag ${IMAGE_NAME}:${BUILD_TAG} ${ECR_REPO}:${BUILD_TAG}"
                    sh "docker tag ${IMAGE_NAME}:${BUILD_TAG} ${ECR_REPO}:latest"
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}"
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh "docker push ${ECR_REPO}:${BUILD_TAG}"
                    sh "docker push ${ECR_REPO}:latest"
                }
            }
        }

        stage('Deploy to Production EC2') {
            steps {
                script {
                
                    sh """
                        ssh -o StrictHostKeyChecking=no ${PROD_HOST} '
                            docker pull ${ECR_REPO}:${BUILD_TAG} &&
                            docker rm -f ${CONTAINER_NAME} || true &&
                            docker run -d --name ${CONTAINER_NAME} -p ${PROD_PORT}:5000 ${ECR_REPO}:${BUILD_TAG}
                        '
                    """
                }
            }
        }

        stage('Health Verification') {
            steps {
                script {
                    retry(3) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${PROD_HOST} '
                                curl -f http://localhost:${PROD_PORT}/health
                            '
                        """
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
               
                sh """
                    ssh -o StrictHostKeyChecking=no ${PROD_HOST} '
                        docker rm -f ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} -p ${PROD_PORT}:5000 ${ECR_REPO}:latest
                    '
                """
            }
        }
    }
}

