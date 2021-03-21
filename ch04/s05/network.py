from dependency import DependsOn

class NetworkFactoryModule():
    def __init__(self, name, ip_range='10.0.0.0/16', region='us-central1'):
        self._name = name
        self._network_name = f'{name}-network'
        self._subnet_name = f'{name}-subnet'
        self._ip_range = ip_range
        self._region = region

    def build(self):
        return [
            {
                'google_compute_network': [{
                    self._network_name: [{
                        'name': self._network_name,
                        'auto_create_subnetworks': False
                    }]
                }]
            },
            {
                'google_compute_subnetwork': [{
                    self._network_name: [{
                        'depends_on': [f'google_compute_network.{self._network_name}'],
                        'name': self._subnet_name,
                        'region': self._region,
                        'network': self._network_name,
                        'ip_cidr_range': self._ip_range
                    }]
                }]
            }
        ]
    
    def outputs(self):
        return DependsOn('google_compute_subnetwork', self._network_name, {
            'name': self._network_name,
            'subnet': self._subnet_name,
            'ip_range': self._ip_range
        })