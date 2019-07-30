from configmap2consul.configmap2consul import init_consul_client, configmap_2_consul


def test_consul_client():

    cclient = init_consul_client("http://192.168.99.100:32080")
    assert cclient.scheme == "http"
    assert cclient.http.host == "192.168.99.100"
    assert cclient.http.port == "32080"


def test_run_spring():
    consul_client = init_consul_client("http://192.168.99.100:32080")
    configmap_2_consul(
        namespace="default",
        labels="configmap2consul=True",
        consul_client=consul_client,
        basepath="basepath",
        mode="spring",
        dryrun=False)


def test_run_basic():
    consul_client = init_consul_client("http://192.168.99.100:32080")
    configmap_2_consul(
        namespace="default",
        labels="configmap2consul=True",
        consul_client=consul_client,
        basepath="basepath",
        mode="basic",
        dryrun=False)
