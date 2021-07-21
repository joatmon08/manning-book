class DatabaseServerFactory:
    def __init__(self, name, region='us-central1', size=1, network='default'):
        self.name = name
        self.region = region
        self.size = size
        self.network = network
        self.resources = self._build()

    def _build(self):
        resources = []
        resources.append({
            'google_compute_instance_template': [{
                'db': [
                    {
                        'disk': [
                            {
                                'auto_delete': True,
                                'boot': True,
                                'source_image': 'https://www.googleapis.com/compute/v1/projects/gce-uefi-images/global/images/ubuntu-1804-bionic-v20200317'
                            }
                        ],
                        'lifecycle': [
                            {
                                'create_before_destroy': True
                            }
                        ],
                        'machine_type': 'e2-micro',
                        'name_prefix': f'{self.name}-',
                        'network_interface': [
                            {
                                'network': self.network
                            }
                        ],
                        'region': self.region
                    }
                ]
            }]
        })
        resources.append({
            'google_compute_target_pool': [{
                'db': [
                    {
                        'name': self.name,
                        'region': self.region
                    }
                ]
            }]
        })
        resources.append({
            'google_compute_instance_group_manager': [{
                'db': [
                    {
                        'base_instance_name': self.name,
                        'name': f'{self.name}-manager',
                        'target_pools': [
                                r'${google_compute_target_pool.db.id}'
                        ],
                        'target_size': self.size,
                        'version': [
                            {
                                'instance_template': r'${google_compute_instance_template.db.id}'
                            }
                        ],
                        'zone': f'{self.region}-a'
                    }
                ]
            }]
        })
        return resources
