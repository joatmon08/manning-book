import json
import ipaddress


def _generate_subnet_name(address):
    address_identifier = format(ipaddress.ip_network(
        address).network_address).replace('.', '-')
    return f'network-{address_identifier}'


def google_subnetwork(address, region):
    name = _generate_subnet_name(address)
    return {
        'resource': [
            {
                'google_compute_subnetwork': [
                    {
                        f'{name}': [
                            {
                                'name': name,
                                'ip_cidr_range': address,
                                'region': region,
                                'network': 'default'
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

        config = google_subnetwork(address, region)

        with open(f'{_generate_subnet_name(address)}.tf.json', 'w') as outfile:
            json.dump(config, outfile, sort_keys=True, indent=4)
