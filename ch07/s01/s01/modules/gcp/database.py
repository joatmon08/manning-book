from tags import StandardTags


class DatabaseFactoryModule():
    def __init__(self, name, server, network,
                 environment,
                 region='us-central1',
                 tier='db-e2-micro', deletion_protection=False):
        self._name = name
        self._server = server
        self._tags = StandardTags(environment).tags
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
                        'depends_on': [
                            f'google_compute_instance.{self._server._name}'
                        ],
                        'region': self._region,
                        'database_version': 'POSTGRES_12',
                        'settings': [{
                            'tier': self._tier,
                            'ip_configuration': [{
                                'authorized_networks': [{
                                    'value': f'${{google_compute_instance.{self._server._name}.network_interface.0.access_config.0.nat_ip}}'
                                }]
                            }],
                            'user_labels': self._tags
                        }],
                        'deletion_protection': self._deletion_protection
                    }]
                }]
            }
        ]
