class DatabaseFactoryModule():
    def __init__(self, name,
                 network='default',
                 region='us-central1',
                 tags=None,
                 tier='db-e2-micro',
                 deletion_protection=False):
        self._name = name
        self._tags = tags
        self._network = network
        self._region = region
        self._tier = tier
        self._deletion_protection = deletion_protection

    def build(self):
        return [
            {
                'google_sql_database': [{
                    self._name: [{
                        'name': self._name,
                        'instance': f'${{google_sql_database_instance.{self._name}.name}}'
                    }]
                }]
            },
            {
                'google_sql_database_instance': [{
                    self._name: [{
                        'region': self._region,
                        'database_version': 'POSTGRES_12',
                        'settings': [{
                            'tier': self._tier,
                            'user_labels': self._tags
                        }],
                        'deletion_protection': self._deletion_protection
                    }]
                }]
            }
        ]
