import json


class StandardTags():
    def __init__(self):
        self.resource = {
            'customer': 'my-company',
            'automated': True,
            'cost_center': 123456,
            'business_unit': 'ecommerce'
        }


class GoogleServer:
    def __init__(self, name, network, zone='us-central1-a', tags={}):
        self.name = name
        self.network = network
        self.zone = zone
        self.tags = tags
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
                                    'machine_type': 'f1-micro',
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


if __name__ == "__main__":
    config = GoogleServer(
        name='hello-world', network='default',
        tags=StandardTags().resource)

    with open('main.tf.json', 'w') as outfile:
        json.dump(config.resource, outfile,
                  sort_keys=True, indent=4)
