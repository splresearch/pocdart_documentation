pipeline {
    agent{
        docker {
            image 'pocdart/pocdart_python:latest'
            args '''
            -v /home/shiny/email_queue:/home/shiny/email_queue \
            -v /home/shiny/sms_queue:/home/shiny/sms_queue \
            -v /var/run/docker.sock:/var/run/docker.sock \
            --group-add shiny-apps \
            --name=jenkins_${JOB_BASE_NAME}_${BRANCH_NAME}
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
                sshagent(credentials: ['jenkins_host_user']) {
                    sh '''
                        # host key check
                        ssh-keyscan -H $HOST_ADDRESS >> /home/jenkins/.ssh/known_hosts
                        # copy config into container
                        scp jenkins@$HOST_ADDRESS:/home/pocdart/config/python/sprint_math/config.json /home/pocdart/pocdart_documentation/scrum/tools
                        # copy test board into container
                        scp jenkins@$HOST_ADDRESS:/home/pocdart/config/python/sprint_math/test_board_data.json /home/pocdart/pocdart_documentation/scrum/tools/card_json_archive
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
