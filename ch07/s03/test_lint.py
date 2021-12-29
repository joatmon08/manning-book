import pytest
from main import GCP_PROJECT_USERS, GCPProjectUsers

GROUP_CONFIGURATION_FILE = 'main.tf.json'


@pytest.fixture
def json():
    with open(GROUP_CONFIGURATION_FILE, 'r') as f:
        return f.readlines()


@pytest.fixture
def users():
    return GCP_PROJECT_USERS


@pytest.fixture
def binding():
    return GCPProjectUsers(
        'testing',
        [('test', 'test', 'roles/test')]).resources['resource'][0]


def test_json_configuration_for_indentation(json):
    assert len(json[1]) - len(json[1].lstrip()) == 4, \
        "output JSON with indent of 4"


def test_user_configuration_for_standard_team_name(users):
    for _, member, _ in GCP_PROJECT_USERS:
        assert member.startswith('team-'), \
            "group should always start with `team-`"


def test_authoritative_project_iam_binding(binding):
    assert 'google_project_iam_binding' in binding.keys(), \
        "use `google_project_iam_binding` to add team members to roles"
