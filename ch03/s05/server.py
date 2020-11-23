def google_db_server_group(resources, name, region='us-central1', size=1, network='default'):
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
                    'machine_type': 'f1-micro',
                    'name_prefix': f'{name}-',
                    'network_interface': [
                        {
                            'network': network
                        }
                    ],
                    'region': region
                }
            ]
        }
        ]
    })
    resources.append({
        'google_compute_target_pool': [{
            'db': [
                {
                    'name': name,
                    'region': region
                }
            ]
        }
        ]
    })
    resources.append(
        {
            'google_compute_instance_group_manager': [
                {
                    'db': [
                        {
                            'base_instance_name': name,
                            'name': f'{name}-manager',
                            'target_pools': [
                                r'${google_compute_target_pool.db.id}'
                            ],
                            'target_size': size,
                            'version': [
                                {
                                    'instance_template': r'${google_compute_instance_template.db.id}'
                                }
                            ],
                            'zone': f'{region}-a'
                        }
                    ]
                }
            ]
        }
    )
