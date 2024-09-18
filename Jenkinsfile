pipeline {
    agent{
        docker {
            image 'pocdart/pocdart_python:latest'
            args '''
            -v /home/shiny/email_queue:/home/shiny/email_queue \
            -v /home/shiny/sms_queue:/home/shiny/sms_queue \
            -v /var/run/docker.sock:/var/run/docker.sock \
            --group-add shiny-apps \
            --name=zoom_api_jenkins
            '''
        }
    }
    stages {
        stage('Build') {
            steps {
                sh '''
                    # clone in target repository
                    cd /home/pocdart && git clone https://github.com/splresearch/pocdart_documentation.git
                    cd /home/pocdart/pocdart_documentation && git checkout $BRANCH_NAME
                ''' 
                sshagent(credentials: ['jenkins_sp-dmaras2']) {
                    sh '''
                        # host key check
			ssh-keyscan -H 10.214.16.64 >> /home/jenkins/.ssh/known_hosts
                        # copy config into container
                        scp jenkins@10.214.16.64:/home/pocdart/config/python/sprint_math/config.json /home/pocdart/pocdart_documentation/scrum/tools
                        # copy test board into container
                        scp jenkins@10.214.16.64:/home/pocdart/config/python/sprint_math/test_board_data.json /home/pocdart/pocdart_documentation/scrum/tools/card_json_archive
                    '''
                }
            }
        }
        stage('Unit Tests') {
            steps {
                sh '''cd /home/pocdart/pocdart_documentation/scrum/tools && python -m pytest tests'''
            }
        }
        stage('Integration Tests') {
            steps {
                echo 'integration tests'
            }
        }
        stage('Deploy') {
            steps {
                echo 'deploy'
            }
        }
    }
}
