
class ConfigMap:

    config_map = {}

    def __init__(self, cmap):
        self.config_map = cmap

    def name(self):
        return str(self.config_map['metadata']['name'])

    def data(self):
        return self.config_map['data']

    def self_link(self):
        return str(self.config_map['metadata']['self_link'])

    def resource_version(self):
        return str(self.config_map['metadata']['resource_version'])
