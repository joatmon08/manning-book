import pytest
import os
import compute
import json

ENVIRONMENTS = ['testing', 'prod']
CONFIGURATION_FILE = 'main.tf.json'

PROJECT = os.environ['CLOUDSDK_CORE_PROJECT']


@pytest.fixture(scope="module")
def configuration():
    merged = []
    for environment in ENVIRONMENTS:
        with open(f'{environment}/{CONFIGURATION_FILE}', 'r') as f:
            environment_configuration = json.load(f)
            merged += environment_configuration['resource']
    return merged


def resources(configuration, resource_type):
    resource_list = []
    for resource in configuration:
        if resource_type in resource.keys():
            resource_name = list(
                resource[resource_type].keys())[0]
            resource_list.append(
                resource[resource_type]
                [resource_name])
    return resource_list


@pytest.fixture
def servers(configuration):
    return resources(configuration,
                     'google_compute_instance')


def test_cpu_size_less_than_or_equal_to_limit(servers):
    CPU_LIMIT = 32
    non_compliant_servers = []
    for server in servers:
        type = compute.get_machine_type(
            PROJECT, server['zone'],
            server['machine_type'])
        if type.cpus > CPU_LIMIT:
            non_compliant_servers.append(server['name'])
    assert len(non_compliant_servers) == 0, \
        f'Servers found using over {CPU_LIMIT}' + \
        f' vCPUs: {non_compliant_servers}'
