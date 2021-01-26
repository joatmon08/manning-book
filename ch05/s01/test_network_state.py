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
        for resource in state['planned_values']['root_module']['resources']:
            if resource['type'] == resource_type:
                return resource
    return _get_resource


def test_state_of_network_for_name(state, resource):
    network = resource(state, 'google_compute_network')
    assert network['values']['name'] == expected_network_name


def test_state_of_subnetwork_for_parameters(state, resource):
    subnet = resource(state, 'google_compute_subnetwork')
    assert subnet['values']['name'] == 'hello-world-subnet'
    assert subnet['values']['network'] == expected_network_name
    assert subnet['values']['ip_cidr_range'] == '10.0.0.0/16'
    assert subnet['values']['region'] == 'us-central1'
