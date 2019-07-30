#!/bin/bash


build(){
    docker build . -f docker/Dockerfile -t aroundthecode/configmap2consul:latest
}

consul(){
    docker run --name test-consul -d -p 8500:8500/tcp -e 'CONSUL_LOCAL_CONFIG={"bootstrap_expect":1,"server":true}' consul agent -ui -server -bind=127.0.0.1 -client=0.0.0.0
}

test(){
	pytest --flake8 --cov=configmap2consul --cov-report term-missing --ignore='tests/test_minikube.py'
}

start_minikube(){
    minikube start --memory 10240 --cpus 4 --kubernetes-version v1.12.4 --feature-gates="PersistentLocalVolumes=true"
}

test_minikube(){
    echo "create minikube elements"
	kubectl apply -f tests/minikube/consul.yaml
	kubectl apply -f tests/minikube/configmaps.yaml
	echo "sleep 20s to wait consul startup"
	sleep 20
	echo "running tests"
	pytest --flake8 --cov=configmap2consul --cov-report term-missing --consul_url "http://$(minikube ip):32080"
	kubectl delete -f tests/minikube/configmaps.yaml
	kubectl delete -f tests/minikube/consul.yaml
}

test_helm(){
    ##### HELM INSTALL #####
    if [ ! -f /usr/local/bin/helm ]
    then
      # Install Helm:
      wget https://storage.googleapis.com/kubernetes-helm/helm-v2.10.0-linux-amd64.tar.gz
      tar -xvzf helm-v2.10.0-linux-amd64.tar.gz
      sudo mv linux-amd64/helm /usr/local/bin/helm
      helm init
    else
      echo "Helm found...skipping install"
    fi
    helm template helm
    helm package helm
    helm install

}
sonar(){
    echo "create minikube elements"
	kubectl apply -f tests/minikube/consul.yaml
	kubectl apply -f tests/minikube/configmaps.yaml
	echo "sleep 20s to wait consul startup"
	sleep 20
	echo "running tests with sonar report format"
    pytest --flake8 --cov=configmap2consul --junitxml tests/junit.xml --cov-report xml  --consul_url "http://$(minikube ip):32080"
    kubectl delete -f tests/minikube/configmaps.yaml
	kubectl delete -f tests/minikube/consul.yaml
    echo "converting coverage in sonar format"
    coverage xml -i
    echo "invoking sonar scanner"
    sonar-scanner -Dsonar.login=${SONAR_TOKEN} -Dsonar.projectKey=aroundthecode_configmap2consul -Dsonar.organization=aroundthecode-github -Dsonar.host.url=https://sonarcloud.io

}
clean(){
	rm -rf wheels dist
	docker rmi -f configmap2consul:test
	docker rmi -f configmap2consul:build
	docker rmi -f aroundthecode/configmap2consul:latest
	docker rm -f test-consul
}

$@