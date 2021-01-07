import credentials
import ipaddress
import json
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


def get_network(name):  # A
    ComputeEngine = get_driver(Provider.GCE)  # A
    driver = ComputeEngine(  # A
        credentials.GOOGLE_SERVICE_ACCOUNT,  # A
        credentials.GOOGLE_SERVICE_ACCOUNT_FILE,  # A
        project=credentials.GOOGLE_PROJECT,  # A
        datacenter=credentials.GOOGLE_REGION)  # A
    return driver.ex_get_subnetwork(  # A
        name, credentials.GOOGLE_REGION)  # A


class ServerFactoryModule:
    def __init__(self, name, network, zone='us-central1-a'):
        self._name = name
        gcp_network_object = get_network(network)  # B
        self._network = gcp_network_object.name  # C
        self._network_ip = self._allocate_last_ip_address_in_range(
            gcp_network_object.cidr)  # C
        self._zone = zone
        self.resources = self._build()

    def _allocate_last_ip_address_in_range(self, ip_range):
        ip = ipaddress.IPv4Network(ip_range)
        return format(ip[-1])

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
                            'subnetwork': self._network,
                            'network_ip': self._network_ip
                        }]
                    }]
                }]
            }]
        }


if __name__ == "__main__":
    server = ServerFactoryModule(name='hello-world', network='default')
    with open('server.tf.json', 'w') as outfile:
        json.dump(server.resources, outfile, sort_keys=True, indent=4)
