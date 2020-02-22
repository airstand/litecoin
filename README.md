# Litecoin 0.17.1 in Docker
This repository contains everything that you need to run Litecoin in Docker and Kubernetes with a simple Jenkins Pipeline script.

## Requirements
- Docker - your Jenkins server needs to have docker binary installed
- kubectl - it should be also available in your Jenkins server
- kubeconfig - separated config for your cluster must be located in ~/.kube/ directory of your Jenkins server (if you are using single kubeconfig you need to edit [Jenkinsfile](https://github.com/airstand/litecoin/blob/master/Jenkinsfile#L27) addinf `--context NAME_OF_CONTEXT` in this repository )


## Dockerfile
Multistage build is picked up as approach. The main reason for this is because I do not want to have everything installed during the build process in the image which will run in Kubernetes. The first image (packager) is built with the single RUN approach. It is because the version of the Litecoin is not going to be change and I am not going to persist different layers for cache purposes. Using `sha256sum -c --strict -` will fail the whole build process if return error. The same will apply for running `python3 shasum.py`.

Build it on your computer - `docker build -t litecoin:0.17.1 .`

## statefulset.yaml
Assumptions
- There is no namespace `litecoin`
- `storageClassName: standard` exist

Additional information
- Using `runAsUser` and `fsGroup` to ensure that I will run with the same user as the one I've created in the Dockerfile
- `dnsConfig` - Adding it always after a huge outage of CoreDNS
- `tolerations` - I am running it in GCP on preemptible nodes
- `resources` - 256MB memory will be enough for Litecoin not in use :)

## Jenkinsfile
This is a very simple Jenkinsfile using Groovy DSL. You need to specify:
- repository
- branch
- full image name (change USERNAME with yours) 
  - `USERNAME/litecoin` - for docker hub
  - `gcr.io/USERNAME/litecoin` for gcp

Please read the Requirements section for additional information about the kubeconfig customizations.