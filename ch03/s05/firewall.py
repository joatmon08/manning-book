class FirewallFactory:
    def __init__(self, name, network='default'):
        self.name = name
        self.network = network
        self.resources = self._build()

    def _build(self):
        resources = []
        resources.append({
            'google_compute_firewall': [{
                'db': [
                    {
                        'allow': [
                            {
                                'protocol': 'tcp',
                                'ports': ['3306']
                            }
                        ],
                        'name': self.name,
                        'network': self.network,
                        'source_ranges': ['0.0.0.0/0']
                    }
                ]
            }
            ]
        })
        return resources
