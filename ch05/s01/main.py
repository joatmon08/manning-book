import json
import netaddr


class NetworkFactoryModule:
    def __init__(self, name,
                 ip_range, number_of_subnets,
                 region='us-central1'):
        self._network_name = f'{name}-network'
        self._subnet_name = f'{name}-subnet'
        self._number_of_subnets = number_of_subnets
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
        ip = netaddr.IPNetwork(self._ip_range)
        subnet_ip_ranges = list(
            ip.subnet(24, count=self._number_of_subnets)
        )
        subnets = []
        for i, subnet_ip in enumerate(subnet_ip_ranges):
            subnets.append({
                f"{self._network_name}-{i}": [{
                    'name': f"{self._subnet_name}-{i}",
                    'region': self._region,
                    'network': self._network_name,
                    'ip_cidr_range': str(subnet_ip)
                }]
            })
        return {
            'google_compute_subnetwork': subnets
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
        name='hello-world',
        ip_range='10.0.0.0/16',
        number_of_subnets=3)
    with open('network.tf.json', 'w') as outfile:
        json.dump(network.resources, outfile,
                  sort_keys=True, indent=4)
