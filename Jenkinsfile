pipeline {
    agent any

    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Recuperation du code source...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installation des dependances...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Linting') {
            steps {
                echo 'Analyse statique du code avec Pylint...'
                sh 'python -m pylint app/ --fail-under=5.0 --output-format=text || true'
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Execution des tests unitaires...'
                sh 'python -m pytest tests/test_crud.py -v --junitxml=reports/unit-tests.xml'
            }
            post {
                always {
                    junit 'reports/unit-tests.xml'
                }
            }
        }

        stage('Integration Tests') {
            steps {
                echo 'Execution des tests d integration...'
                sh 'python -m pytest tests/test_api.py -v --junitxml=reports/integration-tests.xml'
            }
            post {
                always {
                    junit 'reports/integration-tests.xml'
                }
            }
        }

        stage('Coverage') {
            steps {
                echo 'Calcul de la couverture de code...'
                sh '''
                    python -m pytest tests/ --cov=app --cov-report=xml:reports/coverage.xml --cov-report=html:reports/htmlcov --cov-fail-under=80
                '''
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        stage('Code Complexity') {
            steps {
                echo 'Analyse de la complexite avec Radon...'
                sh 'python -m radon cc app/ -a -s'
                sh 'python -m radon mi app/ -s'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Analyse SonarQube...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=product-crud \
                        -Dsonar.sources=app \
                        -Dsonar.tests=tests \
                        -Dsonar.python.coverage.reportPaths=reports/coverage.xml \
                        -Dsonar.python.version=3
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'Verification du Quality Gate SonarQube...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

    }

    post {
        success {
            echo 'Pipeline termine avec succes !'
        }
        failure {
            echo 'Pipeline echoue - verifiez les logs !'
        }
        always {
            echo 'Nettoyage...'
            cleanWs()
        }
    }
}
