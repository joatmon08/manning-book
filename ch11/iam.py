class Module():
    def __init__(self, service,
                 environment,
                 region, project,
                 role):
        self._name = f'{service}-{environment}'
        self._environment = environment
        self._region = region
        self._project = project
        self._role = role

    def build(self):
        return [
            {
                'google_service_account': {
                    self._environment: [
                        {
                            'account_id': self._name,
                            'display_name': self._name
                        }
                    ]
                }
            },
            {
                'google_project_iam_member': {
                    self._environment: {
                        'project': self._project,
                        'role': self._role,
                        'member': 'serviceAccount:' +
                        '${google_service_account.' +
                        f'{self._environment}' + '.email}'
                    }
                }
            }
        ]
