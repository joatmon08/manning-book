# Note: This example will not apply successfully
# with Terraform because it uses mock users and
# groups. However, it will successfully pass a plan.

import json

GCP_PROJECT_USERS = [
    (
        'operations',
        'group:team-operations@example.com',
        'roles/editor'
    ),
    (
        'inventory',
        'group:inventory@example.com',
        'roles/viewer'
    )
]


class GCPProjectUsers:
    def __init__(self, project, users):
        self._project = project
        self._users = users
        self.resources = self._build()

    def _build(self):
        resources = []
        for user, member, role in self._users:
            resources.append({
                'google_project_iam_member': [{
                    user: [{
                        'role': role,
                        'member': member,
                        'project': self._project
                    }]
                }]
            })
        return {
            'resource': resources
        }


if __name__ == "__main__":
    with open('main.tf.json', 'w') as outfile:
        json.dump(GCPProjectUsers(
            'infrastructure-as-code-book',
            GCP_PROJECT_USERS).resources, outfile,
            sort_keys=True, indent=2)
