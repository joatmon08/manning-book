import json
import os
import pytest
from main import generate_json, SERVICE_IMAGE, SERVICE_CONFIGURATION_FILE
import version

expected_service_name = 'hello-world'


@pytest.fixture(scope="module")
def configuration():
    generate_json(expected_service_name)
    with open(SERVICE_CONFIGURATION_FILE, 'r') as f:
        yield json.load(f)
    if os.path.exists(SERVICE_CONFIGURATION_FILE):
        os.remove(SERVICE_CONFIGURATION_FILE)


@pytest.fixture
def resource():
    def _get_resource(configuration, resource_type):
        for resource in configuration['resource']:
            if resource_type in resource.keys():
                return resource[resource_type]
    return _get_resource


@pytest.fixture
def service(configuration, resource):
    return resource(
        configuration,
        'google_cloud_run_service'
    )[0][expected_service_name][0]


@pytest.fixture
def service_iam_member(configuration, resource):
    return resource(
        configuration,
        'google_cloud_run_service_iam_member'
    )[0][expected_service_name][0]


@pytest.mark.unit
def test_configuration_for_service_name(service):
    assert service['name'] == expected_service_name


@pytest.mark.unit
def test_configuration_for_service_version(service):
    assert service['template']['spec']['containers'][
        'image'] == f'{SERVICE_IMAGE}@{version.HELLO}'


@pytest.mark.unit
def test_configuration_for_service_iam_member_role(service_iam_member):
    assert service_iam_member['role'] == 'roles/run.invoker'


@pytest.mark.unit
def test_configuration_for_service_iam_member(service_iam_member):
    assert service_iam_member['member'] == 'allUsers'
