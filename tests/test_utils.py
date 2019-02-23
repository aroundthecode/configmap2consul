import configmap2consul.utils


def test_basic():
    writer = configmap2consul.utils.import_writer("basic")
    assert 'store' in writer.__dict__.keys()


def test_spring():
    writer = configmap2consul.utils.import_writer("spring")
    assert 'store' in writer.__dict__.keys()
