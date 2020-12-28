import adapter


class Network(adapter.NetworkFactory):
    def __init__(self, name, ip_range, region='us-central1'):
        adapter.NetworkFactory.__init__(
            self, name, ip_range, subnet_ip_range=ip_range)
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
                },
                {
                    'google_compute_address': [{
                        self._vpn_name: [{
                            'name': self._vpn_name,
                            'region': self._region
                        }]
                    }]
                },
                {
                    'google_compute_vpn_gateway': [{
                        self._vpn_name: [{
                            'name': self._vpn_name,
                            'network': self._network_name,
                            'region': self._region
                        }]
                    }]
                }
            ]
        }

    def outputs(self):
        return adapter.Network(self._subnet_name, self._ip_range)
