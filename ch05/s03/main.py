import ipaddress

class ServerFactoryModule:
    def __init__(self, name, network, zone='us-central1-a'):
        self._name = name
        self._network = network._network  # D
        self._network_ip = self._allocate_fifth_ip_address(  # D
            network._ip_cidr_range)  # D
        self._zone = zone
        self.resources = self._build()

    def _allocate_fifth_ip_address(self, ip_range):
        ip = ipaddress.IPv4Network(ip_range)
        return format(ip[5])

    def _build(self):
        return {
            'resource': [{
                'google_compute_instance': [{
                    self._name: [{
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
                            'subnetwork': self._network,
                            'network_ip': self._network_ip
                        }]
                    }]
                }]
            }]
        }