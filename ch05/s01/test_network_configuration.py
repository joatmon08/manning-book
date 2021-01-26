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
                return resource[resource_type][0]
    return _get_resource


def test_configuration_of_network_for_name(configuration, resource):
    network = resource(configuration, 'google_compute_network')
    assert network[expected_network_name][0]['name'] == expected_network_name


def test_configuration_of_subnetwork_for_parameters(configuration, resource):
    subnet = resource(configuration, 'google_compute_subnetwork')
    assert subnet[expected_network_name][0]['name'] == 'hello-world-subnet'
    assert subnet[expected_network_name][0]['network'] == expected_network_name
    assert subnet[expected_network_name][0]['ip_cidr_range'] == '10.0.0.0/16'
    assert subnet[expected_network_name][0]['region'] == 'us-central1'
