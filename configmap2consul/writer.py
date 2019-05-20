import logging
from configmap2consul.configmap import ConfigMap
log = logging.getLogger("spring")


class Writer:

    def remove(self, consul_client, keys):
        for key in keys:
            consul_client.kv.delete(key, False)
            log.info("Removed [%s]", key)

    def store(self, consul_client=None, cm: ConfigMap=None, basepath="/", separator="::"):

        try:
            version = cm['metadata']['labels']['version']
            log.info("Found label version=%s on configmap %s, using it for profile", version, cm.name)
            version = separator + version
        except KeyError:
            version = ""

        try:
            subpath = "/" + cm['metadata']['labels']['subpath'] + "/"
            log.info("Found label subpath=%s on configmap %s, using it for subpath", subpath, cm.name)
        except KeyError:
            subpath = "/"

        try:
            app_name = cm['metadata']['labels']['app']
            log.info("Found label app=%s on configmap %s, using it for path", app_name, cm.name)
        except KeyError:
            app_name = cm.name

        ret = []
        for filename in cm.data:
            key = basepath + "/" + app_name + version + subpath + filename
            data = str(cm.data[filename])
            log.debug("Data: %s", data)
            consul_client.kv.put(key, data)
            log.info("Wrote [%s]", key)
            ret.append(key)
        return ret
