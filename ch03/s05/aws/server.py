class DatabaseServerFactory:
    def __init__(self, name,
                 availability_zones=['a'],
                 size=1, network='default'):
        self.name = name
        self.availability_zones = availability_zones
        self.size = size
        self.network = network
        self.data = self._get_data()
        self.resources = self._build()

    def _get_data(self):
        data = []
        data.append({
            'aws_ami': [{
                'ubuntu': [{
                    'most_recent': True,
                    'filter': [
                        {
                            'name': 'name',
                            'values': [
                                'ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*'
                            ]
                        },
                        {
                            'name': 'virtualization-type',
                            'values': [
                                'hvm'
                            ]
                        }
                    ],
                    'owners': [
                        '099720109477'
                    ]
                }]
            }]
        })
        return data

    def _build(self):
        resources = []
        resources.append({
            'aws_launch_template': [{
                'db': [{
                    'name_prefix': self.name,
                    'image_id': '${data.aws_ami.ubuntu.id}',
                    'instance_type': 't2.micro'
                }]
            }]
        })
        resources.append({
            'aws_autoscaling_group': [{
                'db': [{
                    'availability_zones': [f'${{data.aws_region.current.name}}{zone}'
                                           for zone in self.availability_zones],
                    'desired_capacity': self.size,
                    'max_size': self.size,
                    'min_size': self.size,
                    'launch_template': {
                        'id': '${aws_launch_template.db.id}',
                        'version': '$Latest'
                    }
                }]
            }]
        })
        return resources
