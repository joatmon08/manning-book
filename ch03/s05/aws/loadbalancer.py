class LoadBalancerFactory:
    def __init__(self, name,
                 availability_zones=['a'], size=1,
                 external=False):
        self.name = name
        self.availability_zones = availability_zones
        self.size = size
        self.external = external
        self.resources = self._build()

    def _build(self):
        scheme = not self.external
        resources = []
        resources.append({
            'aws_elb': [{
                'db': [{
                    'name': self.name,
                    'availability_zones': [f'${{data.aws_region.current.name}}{zone}'
                                           for zone in self.availability_zones],
                    'internal': scheme,
                    'listener': {
                        'instance_port': 3306,
                        'instance_protocol': 'TCP',
                        'lb_port': 3306,
                        'lb_protocol': 'TCP'
                    },
                    'security_groups': ['${aws_security_group.db.id}']
                }]
            }]
        })
        resources.append({
            'aws_autoscaling_attachment': [{
                'db': [{
                    'autoscaling_group_name': '${aws_autoscaling_group.db.id}',
                    'elb': '${aws_elb.db.id}'
                }]
            }]
        })
        return resources
