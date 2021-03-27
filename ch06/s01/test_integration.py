from main import generate_json, SERVICE_NAME, SERVICE_CONFIGURATION_FILE
import os
import pytest
import subprocess
import terraform


@pytest.fixture(scope='session')
def apply_changes(request):
    service = SERVICE_NAME

    def destroy():
        terraform.destroy()
        os.remove(SERVICE_CONFIGURATION_FILE)

    if request.config.option.environment == "test":
        service = f'{SERVICE_NAME}-test'
        request.addfinalizer(destroy)

    generate_json(service)
    assert os.path.exists(SERVICE_CONFIGURATION_FILE)
    ret, _, _ = terraform.initialize()
    assert ret == 0

    return terraform.apply()


@pytest.mark.integration
def test_changes_have_successful_return_code(apply_changes):
    return_code = apply_changes[0]
    assert return_code == 0


@pytest.mark.integration
def test_changes_should_have_no_errors(apply_changes):
    errors = apply_changes[2]
    assert errors == b''


@pytest.mark.integration
def test_changes_should_output_url(apply_changes):
    changes = apply_changes[1].decode(encoding='utf-8').split('\n')
    status = terraform.status(changes)
    assert 'Apply complete!' in status
    _, output, _ = terraform.output('url')
    assert f'https://{SERVICE_NAME}' in str(output)
