pipeline {
    agent {
        label "slack-agent-linux"
    }

    environment {
        GIT_CREDENTIALS = 'devops-scm-git-token'

        BASELINE_REPO = 'https://github.itops.com/scm/ci/gitops-openstack-autobot-baseline.git'
        BASELINE_BRANCH = 'master'
        BASELINE_CMD = './newconfig.py'
        OS_AUTH_URL = 'https://dashboard.devops.com:5000'
        OS_PROJECT_ID = 'project ID'
        OS_PROJECT_NAME = 'Admin'
        OS_USER_DOMAIN_NAME = 'Cloud'
        OS_PROJECT_DOMAIN_ID = 'Project Domain'
        OS_REGION_NAME = 'us-east-1'
        OS_INTERFACE = 'public'
        OS_IDENTITY_API_VERSION = '3'

        /*
         * Slack Utility Repository
         */
        SLACK_DIR = './SLACK'
        SLACK_REPO = 'https://github.devops.com/scm/ita/utility-slack.git'
        SLACK_BRANCH = 'master'
        SLACK_HEADER_MESSAGE = 'Openstack VM Search Results Summary'
        SLACK_TRAILER_MESSAGE = 'Any closing remarks can go here'
        SLACK_ERRORS_CMD = './slack.py post-file-content-to-slack --source ../result/errors.txt'
        SLACK_FAILURE_CMD = './slack.py post-message-to-slack --message "Failure: Jenkins VM Search Failed"'
        SLACK_SUCCESS_CMD = './slack.py post-csv-to-slack --source ../result'
    }

    parameters {
        string(name: 'ip_address', defaultValue: '10.0.104.105', description: 'Public IP address of the Openstack Vm')
        string(name: 'response_url', defaultValue: '', description: 'Slack response URL')
    }

    stages {
        stage('Fetch Baseline Repo') {
            steps {
                /*
                 * Get the baseline code from the git repo.
                 * This will overwrite the current working
                 * directory contents.
                 */
                git branch: "${env.BASELINE_BRANCH}",
                credentialsId: "${env.GIT_CREDENTIALS}",
                url: "${env.BASELINE_REPO}"
            }
        }

        stage('Fetch Slack Utility Repo') {
            steps {
                /*
                 * Get the code from the slack utility repo.
                 */
                dir("${env.SLACK_DIR}") {
                    git branch: "${env.SLACK_BRANCH}",
                    credentialsId: "${env.GIT_CREDENTIALS}",
                    url: "${env.SLACK_REPO}"
                }
            }
        }

        stage('Find VM Details') {

            steps {
                withCredentials([usernamePassword(credentialsId: 'openstack-autobot-integration', usernameVariable: 'OS_USERNAME', passwordVariable: 'OS_PASSWORD')]) {
                  sh "mkdir -p ${env.WORKSPACE}/result"
                  sh "${env.BASELINE_CMD} $ip_address"
                }
            }
            post {
                success {
                    /*
                     * Post the result file to slack
                     */
                    dir("${env.SLACK_DIR}") {
                        sh "${env.SLACK_SUCCESS_CMD}"
                    }
                }
                failure {
                    /*
                     * Post the failure message to slack
                     */
                    dir("${env.SLACK_DIR}") {
                        sh "${env.SLACK_FAILURE_CMD}"
                    }
                }
            }
        }
    }

    post {
        success {
                slackSend channel: 'automation-integration', color: 'good', message: "VM details has been fetched", teamDomain: 'company-name', tokenCredentialId: '24'
        }

        failure {
                slackSend channel: 'automation-integration', color: 'danger', failOnError: true, message: "Could not find the VM details, check IP address", teamDomain: 'company-name', tokenCredentialId: '24'
        }
    }
}
