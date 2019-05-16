import urllib3


urllib3.disable_warnings()


def pytest_addoption(parser):
    parser.addoption("--consul_url", action="store", default="http://localhost:8500")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value_consul_url = metafunc.config.option.consul_url
    if 'consul_url' in metafunc.fixturenames and option_value_consul_url is not None:
        metafunc.parametrize("consul_url", [option_value_consul_url])
