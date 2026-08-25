def pytest_addoption(parser):
    parser.addoption(
        "--chapter",
        action="store",
        default=None,
        help="Limit example tests to one chapter directory, e.g. ch02",
    )
