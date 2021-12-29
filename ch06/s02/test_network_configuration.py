import json
import pytest

NETWORK_CONFIGURATION_FILE = 'network.tf.json'

expected_network_name = 'hello-world-network'


@pytest.fixture(scope="module")
def configuration():
    with open(NETWORK_CONFIGURATION_FILE, 'r') as f:
        return json.load(f)


@pytest.fixture
def resource():
    def _get_resource(configuration, resource_type):
        for resource in configuration['resource']:
            if resource_type in resource.keys():
                return resource[resource_type]
    return _get_resource


@pytest.fixture
def network(configuration, resource):
    return resource(configuration, 'google_compute_network')[0]


@pytest.fixture
def subnets(configuration, resource):
    return resource(configuration, 'google_compute_subnetwork')


def test_configuration_for_network_name(network):
    assert network[expected_network_name][0]['name'] \
        == expected_network_name


def test_configuration_for_three_subnets(subnets):
    assert len(subnets) == 3


def test_configuration_for_subnet_ip_ranges(subnets):
    for i, subnet in enumerate(subnets):
        assert subnet[next(iter(subnet))
                      ][0]['ip_cidr_range'] == f"10.0.{i}.0/24"
