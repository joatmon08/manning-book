from libcloud.compute.types import NodeState
from main import generate_json, SERVER_CONFIGURATION_FILE
import os
import pytest
import test_utils

TEST_SERVER_NAME = 'hello-world-test'


@pytest.fixture(scope='session')
def apply_changes():
    generate_json(TEST_SERVER_NAME)
    assert os.path.exists(SERVER_CONFIGURATION_FILE)
    assert test_utils.initialize() == 0
    yield test_utils.apply()
    assert test_utils.destroy() == 0
    os.remove(SERVER_CONFIGURATION_FILE)


def test_changes_have_successful_return_code(apply_changes):
    return_code = apply_changes[0]
    assert return_code == 0


def test_changes_should_have_no_errors(apply_changes):
    errors = apply_changes[2]
    assert errors == b''


def test_changes_should_add_1_resource(apply_changes):
    output = apply_changes[1].decode(encoding='utf-8').split('\n')
    assert 'Apply complete! Resources: 1 added, ' + \
        '0 changed, 0 destroyed' in output[-2]


def test_server_is_in_running_state(apply_changes):
    gcp_server = test_utils.get_server(TEST_SERVER_NAME)
    assert gcp_server.state == NodeState.RUNNING
