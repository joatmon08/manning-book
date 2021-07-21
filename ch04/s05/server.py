from dependency import DependsOn
import ipaddress

class ServerFactoryModule():
    def __init__(self, name, zone='us-central1-a', depends_on = None):
        self._name = name
        self._zone = zone
        if depends_on is None:
            self._depends_on = []
        else:
            self._depends_on = [f'{depends_on.resource_type}.{depends_on.resource_id}']
            self._network = depends_on.attributes['name']
            self._subnet = depends_on.attributes['subnet']
            self._network_ip = self._allocate_fifth_ip_address_in_range(depends_on.attributes['ip_range'])
    
    def _allocate_fifth_ip_address_in_range(self, ip_range):
        ip = ipaddress.IPv4Network(ip_range)
        return format(ip[5])

    def build(self):
        return [
            {
                'google_compute_instance': [{
                    self._name: [{
                        'depends_on': self._depends_on,
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
                            'subnetwork': self._subnet,
                            'network_ip': self._network_ip
                        }],
                        'tags': [f"h{self._network_ip.replace('.', '')}"]
                    }]
                }]
            }
        ]
    
    def outputs(self):
        return DependsOn('google_compute_instance', self._name, {
            'name': self._name,
            'network': self._network,
            'ip_address': self._network_ip
        })