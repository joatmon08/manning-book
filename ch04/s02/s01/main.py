import json


class NetworkModuleOutput:
    def __init__(self):
        with open('network/terraform.tfstate', 'r') as network_state:
            network_attributes = json.load(network_state)
        self.name = network_attributes['outputs']['name']['value']


class ServerFactoryModule:
    def __init__(self, name, zone='us-central1-a'):
        self._name = name
        self._network = NetworkModuleOutput()
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
                            'subnetwork': self._network.name
                        }]
                    }]
                }]
            }]
        }


if __name__ == "__main__":
    server = ServerFactoryModule(name='hello-world')
    with open('main.tf.json', 'w') as outfile:
        json.dump(server.resources, outfile, sort_keys=True, indent=4)
