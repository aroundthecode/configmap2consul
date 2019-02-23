
def import_writer(name):
    writer = "configmap2consul.writers." + name
    mod = __import__(writer, fromlist=['Writer'])
    klass = getattr(mod, 'Writer')
    return klass
