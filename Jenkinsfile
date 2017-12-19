properties([
    [$class: 'org.jenkinsci.plugins.github_branch_source.BranchDiscoveryTrait', strategyId: 2]
])
podTemplate(
    label: 'jenkins-pipeline',
    containers: [
        containerTemplate(name: 'jnlp', image: 'lachlanevenson/jnlp-slave:3.10-1-alpine', args: '${computer.jnlpmac} ${computer.name}', workingDir: '/home/jenkins', resourceRequestCpu: '200m', resourceLimitCpu: '300m', resourceRequestMemory: '256Mi', resourceLimitMemory: '512Mi'),
        containerTemplate(name: 'helm', image: 'lachlanevenson/k8s-helm:v2.6.0', command: 'cat', ttyEnabled: true, serviceAccount: 'ci-jenkins'),
        containerTemplate(name: 'kubectl', image: 'lachlanevenson/k8s-kubectl:v1.4.8', command: 'cat', ttyEnabled: true, serviceAccount: 'ci-jenkins')
    ],
    volumes: [
        hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock')
    ]
){
    node('jenkins-pipeline') {
       stage('build') {
           container('jnlp') {
               println "This is build"
           }
       }
       stage('test') {
           container('jnlp') {
               println "This is test"
           }
       }
       stage('deploy') {
           container('jnlp') {
               println "This is deploy"
           }
       }
    }
}
