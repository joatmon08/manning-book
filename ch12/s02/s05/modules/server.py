from . import tags


def build(name, environment, machine_type, zone,
          network='default', long_term=False):
    labels = tags.DefaultTags(
        environment, long_term).get()
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
