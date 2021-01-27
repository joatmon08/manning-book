import pytest
from main import NetworkFactoryModule

NETWORK_PREFIX = 'hello-world'
NETWORK_IP_RANGE = '10.0.0.0/16'


@pytest.fixture(scope="module")
def network():
    return NetworkFactoryModule(
        name=NETWORK_PREFIX,
        ip_range=NETWORK_IP_RANGE,
        number_of_subnets=3)


@pytest.fixture
def network_configuration(network):
    return network._network_configuration()['google_compute_network'][0]


@pytest.fixture
def subnet_configuration(network):
    return network._subnet_configuration()[
        'google_compute_subnetwork']


def test_configuration_for_network_name(network, network_configuration):
    assert network_configuration[network._network_name][
        0]['name'] == f"{NETWORK_PREFIX}-network"


def test_configuration_for_three_subnets(subnet_configuration):
    assert len(subnet_configuration) == 3


def test_configuration_for_subnet_ip_ranges(subnet_configuration):
    for i, subnet in enumerate(subnet_configuration):
        assert subnet[next(iter(subnet))
                      ][0]['ip_cidr_range'] == f"10.0.{i}.0/24"
