from configmap2consul.configmap2consul import init_consul_client


def test_consul_client():

    cclient = init_consul_client("http://192.168.99.100:32080")
    assert cclient.scheme == "http"
    assert cclient.http.host == "192.168.99.100"
    assert cclient.http.port == "32080"
