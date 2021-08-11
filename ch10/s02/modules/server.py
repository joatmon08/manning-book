class ServerFactoryModule():
    def __init__(self, prefix, number,
                 version, zone, labels={}):
        self._name = f'module-{prefix}-{number}'
        self._id = f'module_{version}_{number}'
        self._version = version
        self._tags = labels
        self._zone = zone

    def build(self):
        return {
            'google_compute_instance': {
                self._id: {
                    'depends_on': [
                        'google_compute_subnetwork.' +
                        f'{self._version}'
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
                        'subnetwork':
                        '${google_compute_subnetwork.' +
                        f'{self._version}' + '.name}',
                            'access_config': [{}]
                    }],
                    'labels': self._tags
                }
            }
        }
