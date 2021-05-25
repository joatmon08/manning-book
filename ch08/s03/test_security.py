import json
import pytest
from main import APP_NAME, CONFIGURATION_FILE


@pytest.fixture(scope="module")
def resources():
    with open(CONFIGURATION_FILE, 'r') as f:
        config = json.load(f)
    return config['resource']


@pytest.fixture
def database_firewall_rule(resources):
    return resources[0][
        'google_compute_firewall'][0][APP_NAME][0]


def test_database_firewall_rule_should_not_allow_everything(
        database_firewall_rule):
    assert '0.0.0.0/0' not in \
        database_firewall_rule['source_ranges'], \
        'database firewall rule must not ' + \
        'allow traffic from 0.0.0.0/0, specify source_ranges ' + \
        'with exact IP address ranges'
