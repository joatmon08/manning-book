import pytest
from terraform_runner import (
    apply,
    destroy,
    format_result,
    generate,
    has_terraform_config,
    initialize,
    skip_reason,
)


@pytest.mark.apply
def test_example_applies(directory):
    reason = skip_reason(directory)
    if reason:
        pytest.skip(reason)

    generated = generate(directory)
    assert generated.returncode == 0, format_result(generated)
    assert has_terraform_config(directory), "no Terraform JSON or HCL after generate"

    init = initialize(directory)
    assert init.returncode == 0, format_result(init)

    applied = False
    try:
        result = apply(directory)
        applied = result.returncode == 0
        assert applied, format_result(result)
    finally:
        destroyed = destroy(directory)
        if applied:
            assert destroyed.returncode == 0, format_result(destroyed)
