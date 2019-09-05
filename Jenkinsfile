pipeline {
  agent any
  stages {
    stage('Container Build') {
      parallel {
        stage('Container Build') {
          steps {
            echo 'Building..'
          }
        }
        stage('son-monitor-ceilExp') {
          steps {
            sh 'docker build -t registry.sonata-nfv.eu:5000/son-monitor-ceilexp -f mtrExporter/Dockerfile mtrExporter/'
          }
        }
        stage('son-monitor-libvirtExp') {
          steps {
            sh 'docker build -t registry.sonata-nfv.eu:5000/son-monitor-libvirtexp -f libvirtExporter/Dockerfile libvirtExporter/'
          }
        }
      }
    }
    stage('Unit Tests') {
      steps {
        echo 'Unit Testing..'
      }
    }
    stage('Code Style check') {
      steps {
        echo 'Code Style check....'
      }
    }
    stage('Containers Publication') {
      parallel {
        stage('Containers Publication') {
          steps {
            echo 'Publication of containers in local registry....'
          }
        }
        stage('son-monitor-ceilExp') {
          steps {
            sh 'docker push registry.sonata-nfv.eu:5000/son-monitor-ceilexp'
          }
        }
      }
    }
    
    stage('Promoting containers to integration env') {
      parallel {
        stage('Publishing containers to int') {
          steps {
            echo 'Promoting containers to integration'
          }
        }
        stage('son-monitor-ceilExp') {
          steps {
            sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-ceilexp:latest registry.sonata-nfv.eu:5000/son-monitor-ceilexp:int'
            sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-ceilexp:int'
          }
        }
        stage('son-monitor-libvirtExp') {
          steps {
            sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-libvirtexp:latest registry.sonata-nfv.eu:5000/son-monitor-libvirtexp:int'
            sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-libvirtexp:int'
          }
        }
      }
    }
    stage('Promoting release v5.0') {
        when {
            branch 'v5.0'
        }
        stages {
            stage('Generating release') {
                steps {
                    sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-ceilexp:latest registry.sonata-nfv.eu:5000/son-monitor-ceilexp:v5.0'
                    sh 'docker tag registry.sonata-nfv.eu:5000/son-monitor-libvirtexp:latest registry.sonata-nfv.eu:5000/son-monitor-libvirtexp:v5.0'
                    sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-libvirtexp:v5.0'
                    sh 'docker push  registry.sonata-nfv.eu:5000/son-monitor-ceilexp:v5.0'
                }
            }
        }
    }
  
  }
  post {
    success {
      emailext(subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'", body: """<p>SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                        <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""", recipientProviders: [[$class: 'DevelopersRecipientProvider']])
      
    }
    
    failure {
      emailext(subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'", body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                        <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""", recipientProviders: [[$class: 'DevelopersRecipientProvider']])
      
    }
    
  }
}