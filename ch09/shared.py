import blue

TEAM = 'sundew'
COMPANY = 'dc4plants'
ENVIRONMENT = 'production'
PORT = 8080

shared_name = f'{TEAM}-{ENVIRONMENT}-shared'

def build():
    return load_balancer()

def load_balancer(name=shared_name,
                  blue_zone=blue.zone):
    return [{
            'google_compute_backend_service': {
                TEAM: [{
                    'backend': [{
                        'group': '${google_compute_instance_group.blue.self_link}'
                    }],
                    'health_checks': [
                        f'${{google_compute_health_check.{TEAM}.id}}'
                    ],
                    'load_balancing_scheme': 'INTERNAL_SELF_MANAGED',
                    'locality_lb_policy': 'ROUND_ROBIN',
                    'name': name,
                    'provider': 'google-beta'
                }]
            },
            'google_compute_global_forwarding_rule': {
                TEAM: [{
                    'name': name,
                    'port_range': '80',
                    'target': f'${{google_compute_target_http_proxy.{TEAM}.id}}'
                }]
            },
            'google_compute_health_check': {
                TEAM: [{
                    'http_health_check': [{
                        'port': PORT
                    }],
                    'name': name,
                    'provider': 'google-beta'
                }]
            },
            'google_compute_instance_group': {
                'blue': [{
                    'description': 'Blue server instance group',
                    'instances': [
                        '${google_compute_instance.blue_0.id}',
                        '${google_compute_instance.blue_1.id}',
                        '${google_compute_instance.blue_2.id}'
                    ],
                    'name': blue.server_name,
                    'named_port': [{
                        'name': 'http',
                        'port': f'{PORT}'
                    }],
                    'zone': blue_zone
                }]
            },
            'google_compute_target_http_proxy': {
                TEAM: [{
                    'description': f'Target proxy for {TEAM}',
                    'name': name,
                    'url_map': f'${{google_compute_url_map.{TEAM}.id}}'
                }]
            },
            'google_compute_url_map': {
                TEAM: [{
                    'default_service': f'${{google_compute_backend_service.{TEAM}.id}}',
                    'description': f'URL Map for {TEAM}',
                    'host_rule': [{
                        'hosts': [
                            f'{TEAM}.{COMPANY}.com'
                        ],
                        'path_matcher': 'allpaths'
                    }],
                    'name': name,
                    'path_matcher': [{
                        'default_service': f'${{google_compute_backend_service.{TEAM}.id}}',
                        'name': 'allpaths',
                        'path_rule': [{
                                'paths': [
                                    '/*'
                                ],
                            'service': f'${{google_compute_backend_service.{TEAM}.id}}'
                        }]
                    }]
                }]
            }
            }]
