import json


def standard_tags():
    return {
        'customer': 'my-company',
        'automated': True,
        'cost_center': 123456,
        'business_unit': 'ecommerce'
    }


def google_server(name, network, zone='us-central1-a', tags={}):
    return {
        'resource': [
            {
                'google_compute_instance': [
                    {
                        name: [
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
                                'name': name,
                                'network_interface': [
                                    {
                                        'network': network
                                    }
                                ],
                                'zone': zone,
                                'labels': tags
                            }
                        ]
                    }
                ]
            }
        ]
    }


if __name__ == "__main__":
    config = google_server(
        name='hello-world', network='default', tags=standard_tags())

    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile, sort_keys=True, indent=4)
