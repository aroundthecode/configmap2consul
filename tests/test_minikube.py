from configmap2consul.configmap2consul import init_consul_client, configmap_2_consul
import pytest


def kv_not_set(c, path):
    data = c.kv.get(path)
    assert data[1] is None


def kv_contains(c, path, match):
    data = c.kv.get(path)
    assert match in str(data[1]["Value"])


@pytest.mark.unit
def test_dryrun(consul_url):
    consul_client = init_consul_client(consul_url)
    configmap_2_consul(
        namespace="default",
        labels="configmap2consul=True",
        consul_client=consul_client,
        basepath="basepath",
        dryrun=True)

    # testing dryrun not creating
    kv_not_set(consul_client, "basepath/basic-multiple-configmap.txt/lorem_ipsum-1.txt")


@pytest.mark.unit
def test_run(consul_url):
    consul_client = init_consul_client(consul_url)
    configmap_2_consul(
        namespace="default",
        labels="configmap2consul=True",
        consul_client=consul_client,
        basepath="basepath",
        dryrun=False)

    # testing Single file mode
    kv_contains(consul_client,
                "basepath/basic-simple-configmap/lorem-ipsum.txt",
                "Lorem ipsum")

    # testing multiple file mode
    kv_contains(consul_client,
                "basepath/basic-multiple-configmap/lorem-ipsum-1.txt",
                "Lorem ipsum")

    kv_contains(consul_client,
                "basepath/basic-multiple-configmap/lorem-ipsum-2.txt",
                "Ut enim ad minim veniam")

    # testing version labels
    kv_contains(consul_client,
                "basepath/spring-app::blue/data",
                "color: blue")

    kv_contains(consul_client,
                "basepath/spring-app::orange/data",
                "color: orange")

    kv_contains(consul_client,
                "basepath/spring-noversion/data",
                "color=green")

    # testing subpath labels
    kv_contains(consul_client,
                "basepath/spring-subpath::orange/folder1/data",
                "subpath: folder one")

    kv_contains(consul_client,
                "basepath/spring-subpath::orange/folder2/data",
                "subpath: folder two")

    # Lablel selector not created
    kv_not_set(consul_client, "basepath/spring-minikube::green/data")


@pytest.mark.unit
def test_minikube(consul_url):
    consul_client = init_consul_client(consul_url)
    configmap_2_consul(
        namespace="default",
        labels="release=minikube",
        consul_client=consul_client,
        basepath="basepath",
        dryrun=False)

    kv_contains(consul_client,
                "basepath/spring-minikube::green/data",
                "MORE PROPERTIES")
