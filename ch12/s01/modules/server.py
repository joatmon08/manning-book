import schedule

def build(name, machine_type, zone,
          network='default'):
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
                'resource_policies': [schedule.id()],
                'labels': {
                    'name': name,
                    'purpose':
                    'manning-infrastructure-as-code'
                }
            }
        }
    }
