def build(name, machine_type, zone,
          min, max, cpu_utilization,
          cooldown=60,
          network='default'):
    region = zone.rsplit('-', 1)[0]
    return [{
        'google_compute_instance_template': {
            name: {
                'can_ip_forward': False,
                'disk': {
                    'source_image': 'ubuntu-1804-lts'
                },
                'machine_type': machine_type,
                'name': name,
                'network_interface': {
                    'network': network
                },
                'labels': {
                    'name': name,
                    'purpose':
                    'manning-infrastructure-as-code'
                }
            }
        }
    }, {
        'google_compute_target_pool': {
            name: {
                'name': name,
                'region': region
            }
        }
    }, {
        'google_compute_instance_group_manager': {
            name: {
                'name': name,
                'zone': zone,
                'version': {
                    'instance_template':
                    '${google_compute_instance_template.' +
                    f'{name}.id}}'
                },
                'target_pools': ['${google_compute_target_pool.' +
                                 f'{name}.id}}'
                                 ],
                'base_instance_name': name
            }
        }
    }, {
        'google_compute_autoscaler': {
            name: {
                'name': name,
                'zone': zone,
                'target': '${google_compute_instance_group_manager.' +
                f'{name}.id}}',
                'autoscaling_policy': {
                    'max_replicas': max,
                    'min_replicas': 0,
                    'cooldown_period': cooldown,
                    'cpu_utilization': {
                        'target': cpu_utilization
                    },
                    'scaling_schedules': {
                        'name': 'weekday-scaleup',
                        'min_required_replicas': min,
                        'schedule': '0 6 * * MON-FRI',
                        'duration_sec': '57600',
                        'time_zone': 'US/Central'
                    }
                }
            }
        }
    }]
