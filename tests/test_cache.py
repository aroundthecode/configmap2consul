from configmap2consul.cache import ConfigMapCache


def test_read_write():

    cache = ConfigMapCache()

    key = "mykey"
    value = "myvalue"

    assert cache.read(key) is None

    ret = cache.check_and_add(key, {"version": value})
    assert ret is True
    assert cache.read(key) == {"version": value}

    ret = cache.check_and_add(key, {"version": value})
    assert ret is False


def test_list():

    cache = ConfigMapCache()

    assert cache.list() == []

    cache.write("key1", "one")
    cache.write("key2", "two")
    cache.write("key3", "three")

    cache_list = cache.list()
    assert len(cache_list) == 3
    assert cache_list[0] == "key1"
    assert cache_list[1] == "key2"
    assert cache_list[2] == "key3"

    cache.remove("key2")
    cache_list2 = cache.list()
    assert len(cache_list2) == 2
    assert cache_list2[0] == "key1"
    assert cache_list2[1] == "key3"


def test_array():

    cache = ConfigMapCache()
    cache.write("key1", {"item1": "value1", "item2": "value2"})
    items = cache.read("key1")
    assert items is not None
    assert items['item1'] == "value1"
    assert items['item2'] == "value2"
