class Module():
    def __init__(self, service, environment,
                 zone, machine_type='e2-micro'):
        self._name = f'{service}-{environment}'
        self._environment = environment
        self._zone = zone
        self._machine_type = machine_type

    def build(self):
        return [
            {
                'google_compute_instance': {
                    self._environment: {
                        'allow_stopping_for_update': True,
                        'boot_disk': [{
                            'initialize_params': [{
                                'image': 'ubuntu-1804-lts'
                            }]
                        }],
                        'machine_type': self._machine_type,
                        'name': self._name,
                        'zone': self._zone,
                        'network_interface': [{
                            'subnetwork':
                            '${google_compute_subnetwork.' +
                            f'{self._environment}' + '.name}',
                            'access_config': {
                                'network_tier': 'STANDARD'
                            }
                        }],
                        'service_account': [{
                            'email': '${google_service_account.' +
                            f'{self._environment}' + '.email}',
                            'scopes': ['cloud-platform']
                        }]
                    }
                }
            }
        ]
