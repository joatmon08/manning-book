import pytest
from examples import example_id, iter_examples


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "plan: generate JSON and run terraform plan"
    )
    config.addinivalue_line(
        "markers", "apply: terraform apply then destroy"
    )


def pytest_generate_tests(metafunc):
    if "directory" not in metafunc.fixturenames:
        return
    chapter = metafunc.config.getoption("--chapter")
    examples = list(iter_examples(chapter))
    if not examples:
        metafunc.parametrize(
            "directory",
            [
                pytest.param(
                    None,
                    marks=pytest.mark.skip(
                        reason=f"no examples for {chapter or 'repository'}"
                    ),
                )
            ],
        )
        return
    metafunc.parametrize(
        "directory",
        examples,
        ids=[example_id(path) for path in examples],
    )
