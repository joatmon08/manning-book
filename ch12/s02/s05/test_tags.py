import pytest
import json

CONFIGURATION_FILE = 'main.tf.json'
exemptionS = 'exemptions.json'


@pytest.fixture(scope="module")
def configuration():
    with open(CONFIGURATION_FILE, 'r') as f:
        return json.load(f)


@pytest.fixture(scope='module')
def exemptions():
    with open(exemptionS, 'r') as f:
        return json.load(f)


@pytest.fixture
def servers(configuration):
    servers = dict()
    for resource in configuration['resource']:
        if 'google_compute_instance' in resource.keys():
            servers.update(resource['google_compute_instance'])
    return servers


@pytest.fixture
def server_exemptions(exemptions):
    return exemptions['google_compute_instance']


def test_all_nonprod_resources_should_have_expiration_tag(
        servers, server_exemptions):
    noncompliant = []
    for name, values in servers.items():
        if 'expiration' not in values['labels'].keys() and \
                name not in server_exemptions:
            noncompliant.append(name)
    assert len(noncompliant) == 0, \
        'all nonprod resources should have ' + \
        f'expiration tag, {noncompliant}'
