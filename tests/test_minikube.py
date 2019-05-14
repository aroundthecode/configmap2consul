from configmap2consul.configmap2consul import init_consul_client, configmap_2_consul
import pytest


@pytest.mark.unit
def test_run_spring(consul_url):
    consul_client = init_consul_client(consul_url)
    configmap_2_consul(
        namespace="default",
        labels="configmap2consul=True",
        consul_client=consul_client,
        basepath="basepath",
        mode="spring",
        dryrun=False)


@pytest.mark.unit
def test_run_basic(consul_url):
    consul_client = init_consul_client(consul_url)
    configmap_2_consul(
        namespace="default",
        labels="configmap2consul=True",
        consul_client=consul_client,
        basepath="basepath",
        mode="basic",
        dryrun=False)
