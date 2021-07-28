import json
import pytest

"""
To generate the planned state configuration file, run
`terraform plan -out tfplan`.
Then, render the plan to a JSON file.
`terraform show -json tfplan > plan.json`
"""
PLAN = 'plan.json'


@pytest.fixture(scope="module")
def plan():
    with open(PLAN, 'r') as f:
        return json.load(f)


@pytest.fixture
def resource():
    def _get_resource(plan, resource_type):
        resources = []
        for resource in plan['resource_changes']:
            if resource['type'] == resource_type:
                resources.append(resource)
        return resources
    return _get_resource


@pytest.fixture
def database(plan, resource):
    return resource(plan, 'google_sql_database_instance')[0]

def test_if_plan_deletes_database(database):
    assert database['change']['actions'][0] != 'delete'
