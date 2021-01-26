import pytest
from network import NetworkFactoryModule

NETWORK_PREFIX = 'hello-world'
NETWORK_IP_RANGE = '10.0.0.0/16'


@pytest.fixture(scope="module")
def network():
    return NetworkFactoryModule(
        name=NETWORK_PREFIX, ip_range=NETWORK_IP_RANGE)


def test_network_factory_creates_correct_network_configuration(network):
    network_configuration = network._network_configuration()[
        'google_compute_network'][0]
    assert network_configuration[network._network_name][
        0]['name'] == f"{NETWORK_PREFIX}-network"


def test_network_factory_creates_correct_subnet_configuration(network):
    subnet_configuration = network._subnet_configuration()[
        'google_compute_subnetwork'][0]
    assert subnet_configuration[network._network_name][
        0]['name'] == f"{NETWORK_PREFIX}-subnet"
    assert subnet_configuration[network._network_name][
        0]['network'] == f"{NETWORK_PREFIX}-network"
    assert subnet_configuration[network._network_name][0]['ip_cidr_range'] == NETWORK_IP_RANGE
    assert subnet_configuration[network._network_name][0]['region'] == 'us-central1'
