from tags import StandardTags


class ServerFactoryModule():
    def __init__(self, name, environment,
                 network, zone='us-central1-a'):
        self._name = name
        self._tags = StandardTags(environment).tags
        self._zone = zone
        self._network = network

    def build(self):
        return [
            {
                'google_compute_instance': [{
                    self._name: [{
                        'depends_on': [
                            f'google_compute_subnetwork.{self._network._network_name}'
                        ],
                        'allow_stopping_for_update': True,
                        'boot_disk': [{
                            'initialize_params': [{
                                'image': 'ubuntu-1804-lts'
                            }]
                        }],
                        'machine_type': 'e2-micro',
                        'name': self._name,
                        'zone': self._zone,
                        'network_interface': [{
                            'subnetwork': self._network._subnet_name,
                            'access_config': [{}]
                        }],
                        'labels': self._tags
                    }]
                }]
            }
        ]
