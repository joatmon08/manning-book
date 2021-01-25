class NetworkFacade:  # A
    def __init__(self, network, ip_cidr_range):
        self._network = network
        self._ip_cidr_range = ip_cidr_range


class NetworkFactoryModule:
    def __init__(self, name, ip_range, region='us-central1'):
        self._network_name = f'{name}-network'
        self._subnet_name = f'{name}-subnet'
        self._ip_range = ip_range
        self._region = region
        self.resources = self._build()

    def _build(self):
        return {
            'resource': [
                {
                    'google_compute_network': [{
                        self._network_name: [{
                            'name': self._network_name,
                            'auto_create_subnetworks': False
                        }]
                    }]
                },
                {
                    'google_compute_subnetwork': [{
                        self._network_name: [{
                            'name': self._subnet_name,
                            'region': self._region,
                            'network': self._network_name,
                            'ip_cidr_range': self._ip_range
                        }]
                    }]
                }
            ]
        }

    def outputs(self):
        return NetworkFacade(self._subnet_name, self._ip_range)  # B
