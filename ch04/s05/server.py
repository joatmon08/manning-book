import ipaddress
from network import NetworkFactoryModule


class ServerFactoryModule():
    def __init__(self, name, network='default', zone='us-central1-a'):
        self._name = name
        self._zone = zone
        self._network = network
        self.resources = self._build()

    def _build(self):
        return [
            {
                'google_compute_instance': [{
                    self._name: [{
                        'allow_stopping_for_update': True,
                        'boot_disk': [{
                            'initialize_params': [{
                                'image': 'ubuntu-1804-lts'
                            }]
                        }],
                        'machine_type': 'f1-micro',
                        'name': self._name,
                        'zone': self._zone,
                        'network_interface': [{
                            'network': self._network
                        }]
                    }]
                }]
            }
        ]
