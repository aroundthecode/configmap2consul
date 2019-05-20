from kubernetes import client, config
import logging
import consul
import urllib3
from configmap2consul.cache import ConfigMapCache
from configmap2consul.configmap import ConfigMap
from configmap2consul.writer import Writer

urllib3.disable_warnings()
log = logging.getLogger("configmap2consul")

try:
    config.load_incluster_config()
except Exception as e:
    log.warning("Cannot load in-cluster config, fallback to kube config: [%s]", str(e))
    config.load_kube_config()

k8 = client.CoreV1Api()

cache = ConfigMapCache()
cleanup_cache = ConfigMapCache()
w = Writer()


def configmap_2_consul(
        namespace="default",
        labels="",
        consul_client=None,
        basepath="/",
        separator="::",
        dryrun=True):
    """
    Reads ConfigMap matching give label selector and save them on consul under given base path

    :param namespace: Kubernetes namespace to look for ConfigMaps
    :param labels: label to use as filter
    :param consul_client: consul client used to store k/v
    :param basepath: base path where K7v will be stored
    :param separator: string to use as separator for profile tag
    :param dryrun: if True will just read from Kubernetes but not write to consul
    """
    if labels:
        cmap = k8.list_namespaced_config_map(namespace, label_selector=labels)
    else:
        cmap = k8.list_namespaced_config_map(namespace)

    for i in cmap.to_dict()['items']:

        cm = ConfigMap(i)

        if dryrun:
            log.warning("dryrun - skipping consul write for %s", cm.name)
            store = False
        else:
            store = cache.check_and_add(cm.self_link, {"version": cm.resource_version})

        log.debug("%s - %s - %s -> %s", cm.name, cm.self_link, cm.resource_version, str(store))

        if store:
            items = w.store(consul_client, cm, basepath, separator=separator)
            if len(items) > 0:
                cache.write(
                    cm.self_link,
                    {
                        "version": cm.resource_version,
                        "items": items
                    }
                )
        else:
            log.info("Skipped [%s]", cm.name)

    for i in cache.list():
        if i not in [c['metadata']['self_link'] for c in cmap.to_dict()['items']]:
            if i in cleanup_cache.list():
                log.info("Element [%s] already candidate for eviction, removing", i)
                remove_key = cache.read(i)
                try:
                    remove_key = remove_key['items']
                    w.remove(consul_client, remove_key)
                except KeyError:
                    log.error("Could not find entry 'items' into %s", str(cache.read(i)))
                cleanup_cache.remove(i)
                cache.remove(i)
            else:
                log.info("Element [%s] candidate for eviction, will be removed next loop", i)
                cleanup_cache.write(i, "D")


def init_consul_client(consul_url):
    """
    Init consul client given consul url

    :param consul_url: the url of consul endpoint in form http://consul.domain:port

    :return: initialized consul client
    """
    cproto, chost, cport = consul_url.split(":")
    chost = chost[2:]
    log.debug("scheme=%s host=%s port=%s", cproto, chost, cport)
    consul_client = consul.Consul(host=chost, port=cport, token=None, scheme=cproto, verify=False)
    return consul_client
