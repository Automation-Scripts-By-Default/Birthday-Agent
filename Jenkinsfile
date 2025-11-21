pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'birthday-agent'
        CONTAINER_NAME = 'birthday-agent'
        NETWORK_NAME = 'homelab-network'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Cleanup Workspace') {
            steps {
                echo '🧹 Cleaning workspace...'
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                echo '📥 Checking out code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/LucasDaSilva96/Birthday-Agent.git'
            }
        }

        stage('Verify Prerequisites') {
            steps {
                echo '✅ Verifying prerequisites...'
                script {
                    // Check if homelab-network exists
                    def networkExists = sh(
                        script: "docker network ls | grep ${NETWORK_NAME} || true",
                        returnStdout: true
                    ).trim()
                    
                    if (!networkExists) {
                        echo "⚠️  Network ${NETWORK_NAME} not found, creating it..."
                        sh "docker network create ${NETWORK_NAME}"
                    } else {
                        echo "✅ Network ${NETWORK_NAME} exists"
                    }
                    
                    // Check if MariaDB is running
                    def mariadbRunning = sh(
                        script: "docker ps | grep mariadb || true",
                        returnStdout: true
                    ).trim()
                    
                    if (mariadbRunning) {
                        echo "✅ MariaDB container is running"
                    } else {
                        echo "⚠️  MariaDB container not found - deployment may fail"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                script {
                    sh "docker-compose -f ${COMPOSE_FILE} build"
                }
            }
        }

        stage('Stop Old Container') {
            steps {
                echo '🛑 Stopping old container if exists...'
                script {
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying Birthday Agent...'
                script {
                    sh "docker-compose -f ${COMPOSE_FILE} up -d"
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '🔍 Verifying deployment...'
                script {
                    // Wait a few seconds for container to start
                    sleep(time: 5, unit: 'SECONDS')
                    
                    // Check if container is running
                    def containerRunning = sh(
                        script: "docker ps | grep ${CONTAINER_NAME}",
                        returnStatus: true
                    )
                    
                    if (containerRunning == 0) {
                        echo "✅ Container ${CONTAINER_NAME} is running"
                        
                        // Show container logs
                        echo "📋 Recent logs:"
                        sh "docker logs --tail 20 ${CONTAINER_NAME}"
                    } else {
                        error "❌ Container ${CONTAINER_NAME} failed to start"
                    }
                }
            }
        }

        stage('Cleanup Old Images') {
            steps {
                echo '🧹 Cleaning up old Docker images...'
                script {
                    sh """
                        docker image prune -f || true
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo '📊 Deployment Summary:'
            sh """
                echo "Container Status:"
                docker ps | grep ${CONTAINER_NAME} || echo "Container not running"
                echo ""
                echo "Network Status:"
                docker network inspect ${NETWORK_NAME} --format '{{range .Containers}}{{.Name}} {{end}}' || true
            """
        }
        failure {
            echo '❌ Pipeline failed!'
            echo '📋 Container logs (if available):'
            sh "docker logs --tail 50 ${CONTAINER_NAME} || true"
        }
        always {
            echo '🏁 Pipeline finished'
        }
    }
}