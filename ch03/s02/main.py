import json


class Network:
    def __init__(self, region='us-central1'):
        self._network_name = 'my-network'
        self._subnet_name = f'{self._network_name}-subnet'
        self._subnet_cidr = '10.0.0.0/28'
        self._region = region
        self.resource = self._build()

    def _build(self):
        return {
            'resource': [
                {
                    'google_compute_network': [
                        {
                            f'{self._network_name}': [
                                {
                                    'name': self._network_name
                                }
                            ]
                        }
                    ]
                },
                {
                    'google_compute_subnetwork': [
                        {
                            f'{self._subnet_name}': [
                                {
                                    'name': self._subnet_name,
                                    'ip_cidr_range': self._subnet_cidr,
                                    'region': self._region,
                                    'network': f'${{google_compute_network.{self._network_name}.name}}'
                                }
                            ]
                        }
                    ]
                }
            ]
        }


if __name__ == "__main__":
    network = Network()

    with open(f'main.tf.json', 'w') as outfile:
        json.dump(network.resource, outfile, sort_keys=True, indent=4)
