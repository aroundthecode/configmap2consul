import logging

log = logging.getLogger("spring")


class Writer:

    def remove(self, consul_client, keys):
        for key in keys:
            consul_client.kv.delete(key, False)
            log.info("Removed [%s]", key)

    def store(self, consul_client, cm, basepath, **extras):

        log.debug(extras)

        try:
            ps = extras.get("separator")
        except KeyError:
            ps = "::"

        try:
            version = cm.config_map['metadata']['labels']['version']
            log.info("Found label version=%s on configmap %s, using it for profile", version, cm.name())
            version = ps + version
        except KeyError:
            version = ""

        try:
            subpath = "/" + cm.config_map['metadata']['labels']['subpath'] + "/"
            log.info("Found label subpath=%s on configmap %s, using it for subpath", subpath, cm.name())
        except KeyError:
            subpath = "/"

        try:
            app_name = cm.config_map['metadata']['labels']['app']
            log.info("Found label app=%s on configmap %s, using it for path", app_name, cm.name())
        except KeyError:
            app_name = cm.name()

        ret = []
        if len(cm.data()) > 1:
            log.error("Spring writer can be used only with single file ConfigMap [%s]", cm.name())
        else:
            for filename in cm.data():
                key = basepath + "/" + app_name + version + subpath + filename
                data = str(cm.data()[filename])
                log.debug("Data: %s", data)
                consul_client.kv.put(key, data)
                log.info("Wrote [%s]", key)
                ret.append(key)
        return ret
