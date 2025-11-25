pipeline {
  agent any
  environment {
    REGISTRY = "devilzz"
    IMAGE_NAME = "cloudops-sample-app"
    TAG = "${env.BUILD_NUMBER}"
  }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Build') { steps { sh 'echo Building...' } }
    stage('Test') {
      steps {
        sh '''
          if [ -d "tests" ]; then pytest -q || true; else echo "No tests"; fi
        '''
      }
    }
    stage('Docker Build') {
      steps { sh 'docker build -t ${REGISTRY}/${IMAGE_NAME}:${TAG} .' }
    }
    stage('Docker Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh 'docker push ${REGISTRY}/${IMAGE_NAME}:${TAG}'
          sh 'docker tag ${REGISTRY}/${IMAGE_NAME}:${TAG} ${REGISTRY}/${IMAGE_NAME}:latest || true'
          sh 'docker push ${REGISTRY}/${IMAGE_NAME}:latest || true'
        }
      }
    }
  }
}