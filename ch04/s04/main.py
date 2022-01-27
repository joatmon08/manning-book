# Note: This example will not apply successfully
# with Terraform because it uses mock users and
# groups. However, it will successfully pass a plan.

import json
import access


class GCPIdentityAdapter:
    EMAIL_DOMAIN = 'example.com'

    def __init__(self, metadata):
        gcp_roles = {  # A
            'read': 'roles/viewer',  # A
            'write': 'roles/editor',  # A
            'admin': 'roles/owner'  # A
        }  # A
        self.gcp_users = []
        for permission, users in metadata.items():
            for user in users:
                self.gcp_users.append(
                    (user, self._get_gcp_identity(user),
                        gcp_roles.get(permission)))

    def _get_gcp_identity(self, user):  # B
        if 'team' in user:
            return f'group:{user}@{self.EMAIL_DOMAIN}'
        elif 'automation' in user:
            return f'serviceAccount:{user}@{self.EMAIL_DOMAIN}'
        else:
            return f'user:{user}@{self.EMAIL_DOMAIN}'

    def outputs(self):
        return self.gcp_users


class GCPProjectUsers:  # C
    def __init__(self, project, users):
        self._project = project
        self._users = users
        self.resources = self._build()

    def _build(self):
        resources = []
        for (user, member, role) in self._users:
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
    users = GCPIdentityAdapter(
        access.Infrastructure().resources).outputs()

    with open('main.tf.json', 'w') as outfile:
        json.dump(
            GCPProjectUsers(
                'infrastructure-as-code-book',
                users).resources, outfile, sort_keys=True, indent=4)
