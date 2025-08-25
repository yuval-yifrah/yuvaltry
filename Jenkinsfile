pipeline {
    agent any

    environment {
        IMAGE_NAME     = "my-app"
        ECR_REPO       = "992382545251.dkr.ecr.us-east-1.amazonaws.com/yuvaly"
        AWS_REGION     = "us-east-1"
        BUILD_TAG      = "${BUILD_NUMBER}"
        CONTAINER_NAME = "my-app-main"
        HOST_PORT      = "5000"
        APP_PORT       = "5000"  // הפורט שהאפליקציה שלך מאזינה עליו בתוך הקונטיינר
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
                // עצור והסר קונטיינר קיים אם יש
                sh """
                    if docker ps -q -f name=${CONTAINER_NAME} | grep -q .; then
                        docker stop ${CONTAINER_NAME}
                        docker rm ${CONTAINER_NAME}
                    fi
                """
                
                // הרץ קונטיינר חדש
                sh "docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${APP_PORT} ${ECR_REPO}:${BUILD_TAG}"
            }
        }

        stage('Health Verification') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    echo "Checking if the app is up..."
                    for i in {1..12}; do
                        if curl -s http://localhost:${HOST_PORT}/ > /dev/null; then
                            echo "App is up!"
                            exit 0
                        fi
                        sleep 5
                        echo "Waiting for app to start... attempt \$i"
                    done
                    echo "Health check failed after 1 minute" && exit 1
                """
            }
        }
    }
}

