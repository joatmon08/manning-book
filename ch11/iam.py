class Module():
    def __init__(self, service,
                 environment,
                 region, project):
        self._name = f'{service}-{environment}'
        self._environment = environment
        self._region = region
        self._project = project

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
            }
        ]