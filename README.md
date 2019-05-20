Configmap2Consul
===================

[![Build Status](https://travis-ci.org/aroundthecode/configmap2consul.svg?branch=develop)](https://travis-ci.org/aroundthecode/configmap2consul)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=aroundthecode_configmap2consul&metric=alert_status)](https://sonarcloud.io/dashboard?id=aroundthecode_configmap2consul)


Daemon to pour Kubernetes configmap on consul K/V

This project takes inspiration from [git2consul](https://github.com/breser/git2consul) project, but aims to replace git repositories with Kubernetes ConfigMaps.

It can be used both as a standalone executable or as a docker container (usually a sidecar of Consul itself)

LabelSelector and namespace can be specified in order to filter target ConfigMaps

### Why I wrote this?
git2consul is a great tool and it works like a charm with Spring Cloud Consul libraries but...

I'm not a great fan of storing runtime configuration on version control. 

This brings many problems on your git repository which should take care only to do version control duty:

1) If you have (and I hope you do!) different CI envrionment like dev,test,preprod,etc you will need different configuration branches for each of them, and therefore you have to merge your configuration each time you promote your microservice across them.

2) If you have several microservices (and again, I expect you do!) you will have serveral configuration file so you'll probably end up in having a separate git repository for each microservice code and an **additional** one for **ALL** microservices configuration, which bring management and tracking hell if you want to do release management in a proper way

3) An alternative to point 2 could be having a different git2consul instance for each microservices, this could save your from version control hell, simploy to grag you to network and resources leak maelstrorm

4) If you are a Kubernetes fan you could totally get rid of Git2Consul (or Configmap2Consul as well) and directly mount your configmap into your pods (with is the simplest way of dealing with them) BUT this would trash any advantage you could take from using Spring with Consul: no more real time change and reload for your properties.

###SO..

Trying to save the best of the two world, and looking at a A/B testing release approach, the idea is to save all your properties information in the very same repository as your microservices code and to turn them into a configmap upon new version deploy.

This will eliminate any misalignment between your service code and configuration since they will evolve an be released together.
Once all ConfigMap has been deployed a single instance of Configmap2Consul will take care to pour them all into Consul exaclty where your service is expected to find them for reading
If different version of the same service are deployed at once as dark release, you can manipulate your ConfigMap to store configuration as different K/V entries.

### Release Note

* **v.2.0.0** Only label-based mode (**Breaks breakward compatibility with 1.x if using simple mode** ) 

* **v.1.1.0** Adding subpath management in spring mode

* **v.1.0.0** Working version with 2 mode, simple and spring with version managemente

### Helm Chart
You can find a Helm chart to deploy ConfigMap2Consul as a Consul sidecar under the **helm** folder
###Getting Started

#### Startup dev environment with virtualenv
```bash
./bootstrap.sh
```
All subsequent make commands are supposed to be run withing virtualenv

#### Run test with coverage

In order to run all tests successfully you must first create a Minikube enviroment:

```bash
./make.sh start_minikube
```

Once you have a running minikube instance you can use:

```bash
./make.sh test_minikube
```

This will deploy a full set of ConfigMap samples with different labels set plus a consul instance.

It will then run pytest to start configmap2consul to import all data into consul and verify K/V insertion.

Finally it will cleanup all resources to leave a clean minikube for next test

You can reach consul UI to verify data at http://$(minikube ip):32080/ui

(comment **kubectl delete** command from make.sh if you want your test not to cleanup environment once completed)


#### Build docker image

```bash
./make.sh build
```

Docker image for configmap2Consul will be build and tagged as **configmap2consul:latest**.

Executable will be started as default command, you can use the following environment variables con configure its behaviour 

* **CM2C_INTERVAL** (Default:"5") Polling interval for new ConfigMap detection
* **CM2C_NAMESPACE** (Default:"default") Kubernetes namespace
* **CM2C_LABEL_SELECTOR** (Default:"") Label selector to be applied for filtering (key=value, just one supported at the moment)
* **CM2C_CONSUL_URL** (Default:"http://localhost:8500") Consul url to submit K/V write requests
* **CM2C_CONSUL_PATH** (Default:"test") Default parent path for k/v data (see different mode section for details)

#### Start a containerized consul for testing

```bash
./make.sh consul
```
A docker container with consul will be started and bound to local port 8500
(Deprecated, use minikube deploy instead)


### How things works
Once started configmap2Consul will invoke K8 API in order to retrieve all available ConfigMaps matching given namespace/labelselector and pour information into target Consul server. 

Its best application is in conjunction with [Spring Boot](https://spring.io/projects/spring-boot) microservices using [Spring Cloud Consul](https://spring.io/projects/spring-cloud-consul) to retrieve their configuration from consul.


#### ~~Basic mode~~

Basic mode has been removed since v.2.0.0, you can achieve same behaviour using proper ConfigMaps labeling (see below).

#### Labeling

ConfigMap2Consul will use labels attached to ConfigMaps in order to understand how to import data into consul

* Each file key contained into ConfigMap will become a different key entry into consul

* Base path for all K/V is defined at configmap2consul startup

* Label **app** is used to define the parent folder for all files defined within Configmap 

  E.g. if your configMap containing a file key named "foo.txt", has "app:myservice" label and you configured "test/txt" as your base path, this will be result into /test/txt/myservice/foo.txt containing ConfigMap key data as value.

* Label **version** is used to specify a profile for your app. 
  
  See https://cloud.spring.io/spring-cloud-consul/single/spring-cloud-consul.html#spring-cloud-consul-config for details.
  
  E.g. if your configMap has additional "verson:myversion" label, this will be result into /test/txt/myservice:myversion/foo.txt

  Default profile separator is "::" but can be changed via CLI options *-s* 

  See https://cloud.spring.io/spring-cloud-consul/single/spring-cloud-consul.html#_customizing for details on spring customizations

* Label **"subpath** is used to create additional subfolder into application path.

  E.g. if your configMap has additional "subpath:otherpath" label, this will be result into /test/txt/myservice:myversion/otherpath/foo.txt
    

### Performance and caching
Setting small polling interval provide you very quick consul values update, but can also turn into same properties being written again and again.

So the configmap2consul daemon saves ConfigMap **SelfLink** and **ResourceVersion** in an internal cache, if upon a new polling loop a ConfigMap is already present in cache, the Consul K/V entry will not be overwritten.

This also allows you to edit Consul value for testing before consolidating and persisting them into a new ConfigMap version.

### Cleanup
Once you delete your configmap you expect your consul entry to be cleaned up as well.

ConfigMap2Consul checks cache entries at each iteration, if an entry does not match an existing ConfigMap it's marked as a candidate for eviction. 

If, during next loop, a candidate entry is still missing on kubernetes side it will be removed from consul Key/Value store as well. 