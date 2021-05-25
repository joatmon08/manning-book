class FirewallFactoryModule:
    def __init__(self, name, ports=[],
                 allow_cidr_blocks=[], network='default'):
        self.name = name
        self.network = network
        self.ports = ports
        self.cidr_blocks = allow_cidr_blocks

    def build(self):
        resources = []
        resources.append({
            'google_compute_firewall': [{
                self.name: [
                    {
                        'source_ranges': self.cidr_blocks,
                        'allow': [
                            {
                                'protocol': 'tcp',
                                'ports': self.ports,
                            }
                        ],
                        'name': self.name,
                        'network': self.network
                    }
                ]
            }
            ]
        })
        return resources
