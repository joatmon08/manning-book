from main import generate_json, SERVICE_CONFIGURATION_FILE
import os
import pytest
import requests
import test_utils

TEST_SERVICE_NAME = 'hello-world-test'


@pytest.fixture(scope='session')
def apply_changes():
    generate_json(TEST_SERVICE_NAME)
    assert os.path.exists(SERVICE_CONFIGURATION_FILE)
    assert test_utils.initialize() == 0
    yield test_utils.apply()
    assert test_utils.destroy() == 0
    os.remove(SERVICE_CONFIGURATION_FILE)


@pytest.fixture
def url():
    output, error = test_utils.output('url')
    assert error == b''
    service_url = output.decode(encoding='utf-8').split('\n')[0]
    return service_url


def test_url_for_service_returns_running_page(apply_changes, url):
    response = requests.get(url)
    assert "It's running!" in response.text
