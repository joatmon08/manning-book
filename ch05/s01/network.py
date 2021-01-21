import json


class NetworkFactoryModule:
    def __init__(self, name, ip_range, region='us-central1'):
        self._network_name = f'{name}-network'
        self._subnet_name = f'{name}-subnet'
        self._ip_range = ip_range
        self._region = region
        self.resources = self._build()

    def _network_configuration(self):
        return {
            'google_compute_network': [{
                self._network_name: [{
                    'name': self._network_name,
                    'auto_create_subnetworks': False
                }]
            }]
        }

    def _subnet_configuration(self):
        return {
            'google_compute_subnetwork': [{
                self._network_name: [{
                    'name': self._subnet_name,
                    'region': self._region,
                    'network': self._network_name,
                    'ip_cidr_range': self._ip_range
                }]
            }]
        }

    def _build(self):
        return {
            'resource': [
                self._network_configuration(),
                self._subnet_configuration()
            ]
        }


if __name__ == "__main__":
    network = NetworkFactoryModule(
        name='hello-world', ip_range='10.0.0.0/16')
    with open('network.tf.json', 'w') as outfile:
        json.dump(network.resources, outfile, sort_keys=True, indent=4)
