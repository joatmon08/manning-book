import pytest
from terraform_runner import (
    format_result,
    generate,
    has_terraform_config,
    initialize,
    plan,
    skip_reason,
)


@pytest.mark.plan
def test_example_plans(directory):
    reason = skip_reason(directory)
    if reason:
        pytest.skip(reason)

    generated = generate(directory)
    assert generated.returncode == 0, format_result(generated)
    assert has_terraform_config(directory), "no Terraform JSON or HCL after generate"

    init = initialize(directory)
    assert init.returncode == 0, format_result(init)
    result = plan(directory)
    assert result.returncode == 0, format_result(result)
