import json
import pytest

"""
To generate the planned state configuration file, run
`terraform plan -out tfplan`.
Then, render the plan to a JSON file.
`terraform show -json tfplan > network.state.json`
"""
PLANNED_STATE_CONFIGURATION_FILE = 'network.state.json'

expected_network_name = 'hello-world-network'


@pytest.fixture(scope="module")
def state():
    with open(PLANNED_STATE_CONFIGURATION_FILE, 'r') as f:
        return json.load(f)


@pytest.fixture
def resource():
    def _get_resource(state, resource_type):
        resources = []
        for resource in state['planned_values']['root_module']['resources']:
            if resource['type'] == resource_type:
                resources.append(resource)
        return resources
    return _get_resource


@pytest.fixture
def network(state, resource):
    return resource(state, 'google_compute_network')[0]


@pytest.fixture
def subnets(state, resource):
    return resource(state, 'google_compute_subnetwork')


def test_configuration_for_network_name(network):
    assert network['values']['name'] == expected_network_name


def test_configuration_for_three_subnets(subnets):
    assert len(subnets) == 3


def test_configuration_for_subnet_ip_ranges(subnets):
    for i, subnet in enumerate(subnets):
        assert subnet['values']['ip_cidr_range'] == f"10.0.{i}.0/24"
