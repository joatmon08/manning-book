
from network import NetworkFactoryModule


class FirewallFactoryModule():
    def __init__(self, name, zone='us-central1-a', depends_on=None):
        self._name = name
        self._zone = zone
        self._depends_on = depends_on
        self._server_network = None
        self._server_ip_address = None
        if depends_on is not None:
            self._depends_on = [f'{depends_on.resource_type}.{depends_on.resource_id}']
            self._server_network = depends_on.attributes['network']
            self._server_ip_address = depends_on.attributes['ip_address']

    def build(self):
        return [
            {
                'google_compute_firewall': [{
                    self._name: [{
                        'depends_on': self._depends_on,
                        'name': self._name,
                        'network': self._server_network,
                        'allow': [{
                            'protocol': 'tcp',
                            'ports': ['22']
                        }],
                        'source_ranges': ['0.0.0.0/0'],
                        'target_tags': [f"h{self._server_ip_address.replace('.', '')}"]
                    }]
                }]
            }
        ]
