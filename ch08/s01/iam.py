import re


class ApplicationFactoryModule:
    def __init__(self, name, roles, project):
        self._name = name
        self._roles = roles
        self._project = project
        self.resources = self._build()

    def _set_roles(self):
        role_members = []
        for role in self._roles:
            role_name = re.sub('[^0-9a-zA-Z]+', '-', role)
            role_members.append({
                role_name: {
                    'member':
                    f"serviceAccount:${{google_service_account.{self._name}.email}}",
                    'role': role,
                    'project': self._project
                }
            })
        return role_members

    def _build(self):
        return {
            'google_service_account': [{
                self._name: [{
                    'account_id': self._name
                }]
            }],
            'google_project_iam_member': self._set_roles()
        }
