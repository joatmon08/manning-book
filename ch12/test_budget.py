from estimation import calculate_monthly_compute
from compute import get_machine_type
import pytest
import os
import json

ENVIRONMENTS = ['testing', 'prod']
CONFIGURATION_FILE = 'main.tf.json'

PROJECT = os.environ['CLOUDSDK_CORE_PROJECT']

MONTHTLY_COMPUTE_BUDGET = 4500


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
    servers = dict()
    server_configs = resources(configuration,
                               'google_compute_instance')
    for server in server_configs:
        region = server['zone'].rsplit('-', 1)[0]
        machine_type = server['machine_type']
        key = f'{region},{machine_type}'
        if key not in servers:
            type = get_machine_type(
                PROJECT, server['zone'],
                machine_type)
            servers[key] = {
                'type': type,
                'num_servers': 1
            }
        else:
            servers[key]['num_servers'] += 1
    return servers


def test_monthly_compute_budget_not_exceeded(servers):
    total = 0
    for key, value in servers.items():
        region, _ = key.split(',')
        total += calculate_monthly_compute(value['type'], region) * \
            value['num_servers']
    assert total < MONTHTLY_COMPUTE_BUDGET
