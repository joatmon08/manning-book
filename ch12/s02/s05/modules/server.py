from . import tags


def build(name, environment, machine_type, zone,
          network='default'):
    labels = tags.DefaultTags(
        environment).get()
    print(labels)
    return {
        'google_compute_instance': {
            name: {
                'allow_stopping_for_update': True,
                'zone': zone,
                'boot_disk': [{
                    'initialize_params': [{
                        'image': 'ubuntu-1804-lts'
                    }]
                }],
                'machine_type': machine_type,
                'name': name,
                'network_interface': [{
                    'network': network
                }],
                'labels': labels
            }
        }
    }
