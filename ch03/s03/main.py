import json
import ipaddress


def _generate_subnet_name(address):
    address_identifier = format(ipaddress.ip_network(
        address).network_address).replace('.', '-')
    return f'network-{address_identifier}'


class SubnetFactory:
    def __init__(self, address, region):
        self.name = _generate_subnet_name(address)
        self.address = address
        self.region = region
        self.network = 'default'
        self.resource = self._build()

    def _build(self):
        return {
            'resource': [
                {
                    'google_compute_subnetwork': [
                        {
                            f'{self.name}': [
                                {
                                    'name': self.name,
                                    'ip_cidr_range': self.address,
                                    'region': self.region,
                                    'network': self.network
                                }
                            ]
                        }
                    ]
                }
            ]
        }


if __name__ == "__main__":
    subnets_and_regions = {
        '10.0.0.0/24': 'us-central1',
        '10.0.1.0/24': 'us-west1',
        '10.0.2.0/24': 'us-east1',
    }

    for address, region in subnets_and_regions.items():

        subnetwork = SubnetFactory(address, region)

        with open(f'{_generate_subnet_name(address)}.tf.json', 'w') as outfile:
            json.dump(subnetwork.resource, outfile, sort_keys=True, indent=4)
