import json
import netaddr


def get_subnet_address(cidr_range):
    ip = netaddr.IPNetwork(cidr_range)
    subnets = list(ip.subnet(28, count=4))
    return format(subnets[0])


class Network:
    def __init__(self, network='my-network', cidr_range='10.0.0.0/16', region='us-central1'):
        self._network_name = network
        self._network_cidr = cidr_range
        self._subnet_name = f'{network}-subnet'
        self._subnet_cidr = get_subnet_address(self._network_cidr)
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
