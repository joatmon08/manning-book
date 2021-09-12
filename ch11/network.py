class Module():
    def __init__(self, service, environment,
                 region):
        self._name = f'{service}-{environment}'
        self._environment = environment
        self._region = region
        self._ip_range = '10.0.0.0/24'

    def build(self):
        return [
            {
                'google_compute_network': {
                    self._environment: {
                        'name': self._name,
                        'auto_create_subnetworks': False
                    },
                }
            },
            {
                'google_compute_subnetwork': {
                    self._environment: {
                        'name': self._name,
                        'region': self._region,
                        'network': '${google_compute_network.' +
                        f'{self._environment}' +
                        '.name}',
                        'ip_cidr_range': self._ip_range
                    }
                }
            },
            {
                'google_compute_global_address': {
                    self._environment: {
                        'provider': 'google-beta',
                        'name': self._name,
                        'purpose': 'VPC_PEERING',
                        'address_type': 'INTERNAL',
                        'prefix_length': 24,
                        'network': '${google_compute_network.' +
                        f'{self._environment}' +
                        '.id}'
                    }
                }
            },
            {
                'google_service_networking_connection': {
                    self._environment: {
                        'provider': 'google-beta',
                        'network': '${google_compute_network.' +
                        f'{self._environment}' + '.id}',
                        'service': 'servicenetworking.googleapis.com',
                        'reserved_peering_ranges': [
                            '${google_compute_global_address.' +
                            f'{self._environment}' +
                            '.name}'
                        ]
                    }
                }
            },
        ]
