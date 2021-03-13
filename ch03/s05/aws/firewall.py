class FirewallFactory:
    def __init__(self, name):
        self.name = name
        self.resources = self._build()

    def _build(self):
        resources = []
        resources.append({
            'aws_security_group': [{
                'db': [
                    {
                        'name': self.name,
                        'description': 'Allow to database',
                        'vpc_id': '${data.aws_vpc.default.id}',
                        'ingress': [{
                            'description': 'Allow inbound to database',
                            'from_port': 3306,
                            'to_port': 3306,
                            'protocol': 'tcp',
                            'cidr_blocks': ['0.0.0.0/0'],
                            'ipv6_cidr_blocks': None,
                            'prefix_list_ids': None,
                            'security_groups': None,
                            'self': None
                        }],
                        'egress': [{
                            'description': 'Allow outbound to VPC',
                            'from_port': 0,
                            'to_port': 0,
                            'protocol': '-1',
                            'cidr_blocks': ['${data.aws_vpc.default.cidr_block}'],
                            'ipv6_cidr_blocks': None,
                            'prefix_list_ids': None,
                            'security_groups': None,
                            'self': None
                        }]
                    }
                ]
            }
            ]
        })
        return resources
