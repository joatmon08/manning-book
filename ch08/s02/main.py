class TagsPrototypeModule():
    def __init__(
            self, service, department,
            business_unit, company, team_email,
            environment):
        self.resource = {
            'service': service,
            'department': department,
            'business-unit': business_unit,
            'company': company,
            'email': team_email,
            'environment': environment,
            'automated': True,
            'repository': f"${company}-${service}-infrastructure"
        }


class ServerFactory:
    def __init__(self, name, network, zone='us-central1-a', tags={}):
        self.name = name
        self.network = network
        self.zone = zone
        self.tags = TagsPrototypeModule(
            'frontend', 'web', 12345, 'udress',
            'frontend@udress.net', 'production')
        self.resource = self._build()

    def _build(self):
        return {
            'resource': [
                {
                    'google_compute_instance': [
                        {
                            self.name: [
                                {
                                    'allow_stopping_for_update': True,
                                    'boot_disk': [
                                        {
                                            'initialize_params': [
                                                {
                                                    'image': 'ubuntu-1804-lts'
                                                }
                                            ]
                                        }
                                    ],
                                    'machine_type': 'e2-micro',
                                    'name': self.name,
                                    'network_interface': [
                                        {
                                            'network': self.network
                                        }
                                    ],
                                    'zone': self.zone,
                                    'labels': self.tags
                                }
                            ]
                        }
                    ]
                }
            ]
        }
