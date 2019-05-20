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
	kubectl apply -f tests/minikube/configmap2consul.yaml
	echo "sleep 20s to wait consul startup"
	sleep 20
	echo "running tests"
	pytest --flake8 --cov=configmap2consul --cov-report term-missing --consul_url "http://$(minikube ip):32080"
	kubectl delete -f tests/minikube/configmap2consul.yaml
}

sonar(){
    pytest --flake8 --cov=configmap2consul --junitxml tests/junit.xml --cov-report xml  --consul_url "http://$(minikube ip):32080"
    coverage xml -i
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