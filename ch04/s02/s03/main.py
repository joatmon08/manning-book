import credentials
import ipaddress
import json
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


def get_network(name):
    ComputeEngine = get_driver(Provider.GCE)
    driver = ComputeEngine(
        credentials.GOOGLE_SERVICE_ACCOUNT,
        credentials.GOOGLE_SERVICE_ACCOUNT_FILE,
        project=credentials.GOOGLE_PROJECT,
        datacenter=credentials.GOOGLE_REGION)
    return driver.ex_get_subnetwork(
        name, credentials.GOOGLE_REGION)


class ServerFactoryModule:
    def __init__(self, name, network, zone='us-central1-a'):
        self._name = name
        gcp_network_object = get_network(network)
        self._network = gcp_network_object.name
        self._network_ip = self._allocate_fifth_ip_address_in_range(
            gcp_network_object.cidr)
        self._zone = zone
        self.resources = self._build()

    def _allocate_fifth_ip_address_in_range(self, ip_range):
        ip = ipaddress.IPv4Network(ip_range)
        return format(ip[5])

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
                            'subnetwork': self._network,
                            'network_ip': self._network_ip
                        }]
                    }]
                }]
            }]
        }


if __name__ == "__main__":
    server = ServerFactoryModule(name='hello-world', network='default')
    with open('main.tf.json', 'w') as outfile:
        json.dump(server.resources, outfile, sort_keys=True, indent=4)
