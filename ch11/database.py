class Module():
    def __init__(self, service,
                 environment,
                 region,
                 tier='db-f1-micro',
                 deletion_protection=False):
        self._name = f'{service}-{environment}'
        self._environment = environment
        self._region = region
        self._tier = tier
        self._deletion_protection = deletion_protection

    def build(self):
        return [
            {
                'google_sql_database': {
                    self._environment: {
                        'name': self._name,
                        'instance':
                        '${google_sql_database_instance.' +
                        f'{self._environment}' + '.name}'
                    }
                }
            },
            {
                'google_sql_database_instance': {
                    self._environment: {
                        'depends_on': [
                            'google_service_networking_connection.' +
                            f'{self._environment}'
                        ],
                        'region': self._region,
                        'settings': {
                            'tier': self._tier,
                            'ip_configuration': {
                                'ipv4_enabled': False,
                                'private_network':
                                '${google_compute_network.' +
                                f'{self._environment}' + '.id}'
                            }
                        },
                        'deletion_protection': self._deletion_protection
                    }
                }
            }
        ]
