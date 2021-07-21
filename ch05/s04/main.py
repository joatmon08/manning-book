import json

SERVER_CONFIGURATION_FILE = 'main.tf.json'


class ServerFactoryModule:
    def __init__(self, name, network, zone='us-central1-a'):
        self._name = name
        self._network = network
        self._zone = zone
        self.resources = self._build()

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
                            'network': self._network,
                        }]
                    }]
                }]
            }]
        }


def generate_json(server_name):
    server = ServerFactoryModule(name=server_name,
                                 network='default')
    with open(SERVER_CONFIGURATION_FILE, 'w') as outfile:
        json.dump(server.resources, outfile,
                  sort_keys=True, indent=4)
