pipeline {
    agent any

    environment {
        IMAGE_NAME     = "my-app"
        ECR_REPO       = "992382545251.dkr.ecr.us-east-1.amazonaws.com/yuvaly"
        AWS_REGION     = "us-east-1"
        BUILD_TAG      = "${BUILD_NUMBER}"
        CONTAINER_NAME = "my-app-main"
        HOST_PORT      = "5000"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_TAG} ."
            }
        }

        stage('Test') {
            steps {
                echo "no tests yet, add in the future"
            }
        }

        stage('Tag & Push to ECR') {
            when {
                branch 'main'
            }
            steps {
                sh "docker tag ${IMAGE_NAME}:${BUILD_TAG} ${ECR_REPO}:${BUILD_TAG}"
                sh "docker tag ${IMAGE_NAME}:${BUILD_TAG} ${ECR_REPO}:latest"

                sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}"
                sh "docker push ${ECR_REPO}:${BUILD_TAG}"
                sh "docker push ${ECR_REPO}:latest"
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                sh "docker ps -q -f name=${CONTAINER_NAME} | grep -q . && docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:5000 ${ECR_REPO}:${BUILD_TAG}"
            }
        }

        stage('Health Verification') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    for i in {1..10}; do
                      if curl -s http://localhost:${HOST_PORT}/; then
                        echo "App is up"
                        exit 0
                      fi
                      echo "Waiting for app..."
                      sleep 3
                    done
                    echo "Health check failed" && exit 1
                """
            }
        }
    }
}
