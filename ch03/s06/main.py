import json


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
        return self._network_name


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
                        'machine_type': 'f1-micro',
                        'name': self._name,
                        'zone': self._zone,
                        'network_interface': [{
                            'network': self._network
                        }]
                    }]
                }]
            }]
        }


if __name__ == "__main__":
    network = NetworkFactoryModule(
        name='hello-world', ip_range='10.0.0.0/16')
    with open('network.tf.json', 'w') as outfile:
        json.dump(network.resources, outfile, sort_keys=True, indent=4)

    server = ServerFactoryModule('hello-world', network.outputs())
    with open('server.tf.json', 'w') as outfile:
        json.dump(server.resources, outfile, sort_keys=True, indent=4)
