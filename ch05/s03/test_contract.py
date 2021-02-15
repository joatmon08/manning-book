from network import NetworkFactoryModule, NetworkFacade
import pytest

network_name = 'hello-world'
network_cidr_range = '10.0.0.0/16'


@pytest.fixture
def network_outputs():
    network = NetworkFactoryModule(
        name=network_name,
        ip_range=network_cidr_range)
    return network.outputs()


def test_network_output_is_facade(network_outputs):
    assert isinstance(network_outputs, NetworkFacade)


def test_network_output_has_network_name(network_outputs):
    assert network_outputs._network == f"{network_name}-subnet"


def test_network_output_has_ip_cidr_range(network_outputs):
    assert network_outputs._ip_cidr_range == network_cidr_range
