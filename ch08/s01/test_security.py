import pytest
from main import build_frontend_configuration


@pytest.fixture(scope="module")
def configuration():
    return build_frontend_configuration()


@pytest.fixture
def resource():
    def _get_resource(configuration, resource_type):
        if resource_type in configuration['resource'].keys():
            return configuration['resource'][resource_type]
    return _get_resource


@pytest.fixture
def roles(configuration, resource):
    role_list = []
    for role in resource(configuration, 'google_project_iam_member'):
        role_list.append(list(role.values())[0]['role'])
    return role_list


def test_service_account_should_not_use_project_admin(roles):
    assert 'roles/editor' not in roles
    assert 'roles/owner' not in roles

def test_database_password_marked_as_sensitive(roles):
    assert 'roles/editor' not in roles
