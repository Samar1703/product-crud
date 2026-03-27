pipeline {
    agent any
    environment {
        PYTHONPATH = "${WORKSPACE}"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install') {
            steps { sh 'pip install -r requirements.txt --break-system-packages' }
        }
        stage('Linting') {
            steps { sh 'python -m pylint app/ --fail-under=5.0 || true' }
        }
        stage('Tests') {
            steps { sh 'mkdir -p reports && python -m pytest tests/ -v --cov=app --cov-report=xml:reports/coverage.xml --cov-fail-under=80' }
        }
        stage('Radon') {
            steps { sh 'python -m radon cc app/ -a -s' }
        }
        stage('SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner -Dsonar.projectKey=product-crud -Dsonar.sources=app -Dsonar.tests=tests -Dsonar.python.coverage.reportPaths=reports/coverage.xml -Dsonar.python.version=3'
                }
            }
        }
    }
    post {
        success { echo 'Pipeline OK!' }
        failure { echo 'Pipeline FAIL!' }
    }
}