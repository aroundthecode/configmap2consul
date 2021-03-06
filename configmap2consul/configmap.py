import yaml


class ConfigMap:

    def __init__(self, cmap={}):
        self._config_map = cmap

    @property
    def name(self):
        return str(self._config_map['metadata']['name'])

    @property
    def labels(self):
        return self._config_map['metadata']['labels']

    @property
    def data(self):
        return self._config_map['data']

    @property
    def self_link(self):
        return str(self._config_map['metadata']['self_link'])

    @property
    def resource_version(self):
        return str(self._config_map['metadata']['resource_version'])

    def __str__(self):
        try:
            y = yaml.safe_dump(self._config_map)
            return y
        except yaml.YAMLError:
            return str(self.name)

    def __getitem__(self, item):
        if item not in self._config_map:
            raise KeyError
        return self._config_map[item]
