import logging
from configmap2consul.configmap import ConfigMap

log = logging.getLogger("basic")


class Writer:

    def remove(self, consul_client, keys):
        for key in keys:
            consul_client.kv.delete(key)
            log.info("Removed [%s]", key)

    def store(self, consul_client, cm: ConfigMap, basepath, **extras):

        if len(extras) > 0:
            log.warning("Basic writer doesn't manage extras, they will be ignored")

        ret = []
        for filename in cm.data:
            data = str(cm.data[filename])
            key = basepath + "/" + filename
            log.debug("Data: %s", data)
            consul_client.kv.put(key, data)
            log.info("Wrote [%s]", key)
            ret.append(key)

        return ret
