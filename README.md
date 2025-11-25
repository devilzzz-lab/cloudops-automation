# CloudOps Automation — CI/CD & Monitoring System (sample)
Simple Flask app used for Phase-3 CI/CD demo.

## Build locally
docker build -t <dockerhub-user>/cloudops-sample-app:latest

## Jenkins
Contains Jenkinsfile for pipeline stages: Checkout → Build → Test → Docker Build → Push