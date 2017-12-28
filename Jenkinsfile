#!/usr/bin/groovy

def project = "rtnpro"
def appName = "hellocicd"

def branch = env.BRANCH_NAME
def imageTag = "docker.io/${project}/${appName}:${branch}"
def domain = "${appName}-${branch}${env.HELLOCICD_DOMAIN}"
def namespace = "${appName}-${branch}"
def helmRelease = namespace
def replicas = 2

def canaryReplicas = 1

def stableBranch = 'master'
def stableNamespace = "${appName}-${stableBranch}"

if (env.BRANCH_NAME == stableBranch) {
    domain = "${appName}${env.HELLOCICD_DOMAIN}"    
}

podTemplate(
    label: 'jenkins-pipeline',
    containers: [
        containerTemplate(name: 'jnlp', image: 'lachlanevenson/jnlp-slave:3.10-1-alpine', args: '${computer.jnlpmac} ${computer.name}', workingDir: '/home/jenkins', resourceRequestCpu: '200m', resourceLimitCpu: '300m', resourceRequestMemory: '256Mi', resourceLimitMemory: '512Mi'),
        containerTemplate(name: 'helm', image: 'lachlanevenson/k8s-helm:v2.6.0', command: 'cat', ttyEnabled: true, serviceAccount: 'ci-jenkins'),
        containerTemplate(name: 'kubectl', image: 'lachlanevenson/k8s-kubectl:v1.8.2', command: 'cat', ttyEnabled: true, serviceAccount: 'ci-jenkins')
    ],
    volumes: [
        hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
        persistentVolumeClaim(mountPath: '/home/jenkins', claimName: 'jenkins-workspace')
    ]
){

    node('jenkins-pipeline') {
        checkout scm

        stage('Build') {
            sh "docker build -t ${imageTag} ."

            withCredentials([[$class: 'UsernamePasswordMultiBinding',
                    credentialsId: 'rtnpro-docker-creds',
                    usernameVariable: 'username',
                    passwordVariable: 'password']]) {
                sh "docker login -u ${username} -p ${password}"
                sh "docker push ${imageTag}"
            }
        }

        stage('Deploy') {
            container('helm') {
                sh """
                    helm upgrade --install ${helmRelease} \
                    charts/hellocicd \
                    --namespace ${namespace} \
                    -f charts/hellocicd/Values.yaml --set \
                    serviceType=LoadBalancer,image=${imageTag},domain=${domain},release=${branch},replicas=${replicas}
                    """
            }
        }
    }

    if (env.BRANCH_NAME == 'master') {
        return
    }

    try {
        stage('Canary') {
            input(message: 'Do you want to proceed with canary?')
            node('jenkins-pipeline') {
                container('helm') {
                    sh """
                       helm upgrade --install ${helmRelease}-canary \
                       charts/hellocicd \
                       --namespace ${stableNamespace} \
                       -f charts/hellocicd/Values.yaml --set \
                       enableService=false,image=${imageTag},replicas=${canaryReplicas},release=${branch},track=canary
                        """
                }
            }

            input(message: 'Test canary changes? Rollback canary?')

            node('jenkins-pipeline') {
                container('helm') {
                    sh "helm delete --purge ${canaryHelmRelease}"
                }
            }
        }
    }
    catch (error) {
        println "Skipping canary..."
    }

    stage('Destroy') {
        input(message: 'Do you want to destroy this deployment?')
        node('jenkins-pipeline') {
            container('helm') {
                sh "helm delete --purge ${helmRelease}"
            }

            container('kubectl') {
                sh "kubectl delete namespace ${namespace}"
            }
        }
    }
}
