import json


class NetworkSingleton:
    def __init__(self, name='default', region='us-central1'):
        self.name = name


class ServerFactoryModule:
    def __init__(self, name, zone='us-central1-a'):
        self._name = name
        self._network = NetworkSingleton()
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
                        'machine_type': 'f1-micro',
                        'name': self._name,
                        'zone': self._zone,
                        'network_interface': [{
                            'subnetwork': self._network.name,
                        }]
                    }]
                }]
            }]
        }


if __name__ == "__main__":
    server = ServerFactoryModule(name='hello-world')
    with open('server.tf.json', 'w') as outfile:
        json.dump(server.resources, outfile, sort_keys=True, indent=4)
