import logging

log = logging.getLogger("cache")


class ConfigMapCache:

    cache = {}

    def __init__(self):
        self.cache = {}

    def list(self):
        """
        Return a list of cache keys

        :return: list of cache keys
        """

        return list(self.cache.keys())

    def remove(self, key):
        """
        Remove element from cache by key

        :param key: key to be removed
        :return: removed element, None if key not present
        """
        return self.cache.pop(key, None)

    def read(self, key):
        """
        Read an entry from the cache.

        :param key: key to look for

        :return: value if key is found in cacke, None otherwise
        """
        ret = None
        try:
            ret = self.cache[key]
        except KeyError:
            log.error("no key " + key + " found")
        return ret

    def write(self, key, value):
        """
        Add new key-value to cache.

        :param key: key to add
        :param value: value to add
        """
        self.cache[key] = value

    def check_and_add(self, key, value):
        """
        Check if a key is present in cache, if not adds it.

        :param key: the key to check
        :param value: the value to add

        :return: True if the entry has been added to cache, False if already present
        """
        ret = True
        if key in self.cache and value['version'] == self.read(key)['version']:
            ret = False
        else:
            self.write(key, value)

        return ret
