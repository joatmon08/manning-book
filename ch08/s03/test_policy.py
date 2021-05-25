import json
import pytest
from main import APP_NAME, CONFIGURATION_FILE


@pytest.fixture(scope="module")
def resources():
    with open(CONFIGURATION_FILE, 'r') as f:
        config = json.load(f)
    return config['resource']


@pytest.fixture
def database_instance(resources):
    return resources[2][
        'google_sql_database_instance'][0][APP_NAME][0]


def test_database_instance_should_have_tags(database_instance):
    assert database_instance['settings'][0]['user_labels'] \
        is not None
    assert len(
        database_instance['settings'][0]['user_labels']) > 0, \
        'database instance must have `user_labels`' + \
        'configuration with tags'
