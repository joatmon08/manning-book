import blue
import green
import passive

TEAM = 'sundew'
COMPANY = 'dc4plants'
ENVIRONMENT = 'production'
PORT = 8080

shared_name = f'{TEAM}-{ENVIRONMENT}-shared'

default_version = 'blue'

services_list = [
    {
        'version': 'blue',
        'zone': blue.zone,
        'name': f'{shared_name}-blue',
        'weight': 90
    },
    {
        'version': 'green',
        'zone': green.zone,
        'name': f'{shared_name}-green',
        'weight': 10
    }
    # {
    #     'version': 'passive',
    #     'zone': passive.zone,
    #     'name': f'{shared_name}-passive',
    #     'weight': 0
    # }
]


def build():
    return backend_services(services_list) + \
        load_balancer(shared_name,
                      default_version,
                      services_list)


def backend_services(services):
    backend_services = []
    for service in services:
        name = service['name']
        version = service['version']
        zone = service['zone']
        backend_services.append({
            'google_compute_backend_service': {
                version: [{
                    'backend': [{
                        'group': ('${google_compute_instance_group.'
                                  f'{version}.self_link}}')
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
            'google_compute_instance_group': {
                version: [{
                    'description': f'{version} server instance group',
                    'instances': [
                        f'${{google_compute_instance.{version}_0.id}}',
                        f'${{google_compute_instance.{version}_1.id}}',
                        f'${{google_compute_instance.{version}_2.id}}'
                    ],
                    'name': name,
                    'named_port': [{
                        'name': 'http',
                        'port': f'{PORT}'
                    }],
                    'zone': zone
                }]
            }
        })
    return backend_services


def _generate_backend_services(services):
    backend_services_list = []
    for service in services:
        version = service['version']
        weight = service['weight']
        backend_services_list.append({
            'backend_service': (
                '${google_compute_backend_service.'
                f'{version}.id}}'
            ),
            'weight': weight,
        })
    return backend_services_list


def load_balancer(name, default_version, services):
    return [{
        'google_compute_global_forwarding_rule': {
            TEAM: [{
                'name': name,
                'port_range': '80',
                'target': ('${google_compute_target_http_proxy.'
                           f'{TEAM}.id}}'),
                'load_balancing_scheme': 'INTERNAL_SELF_MANAGED',
                'ip_address': '0.0.0.0'
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
        'google_compute_target_http_proxy': {
            TEAM: [{
                'description': f'Target proxy for {TEAM}',
                'name': name,
                'url_map': f'${{google_compute_url_map.{TEAM}.id}}'
            }]
        },
        'google_compute_url_map': {
            TEAM: [{
                'default_service': (
                    '${google_compute_backend_service.'
                    f'{default_version}.id}}'
                ),
                'description': f'URL Map for {TEAM}',
                'host_rule': [{
                    'hosts': [
                        f'{TEAM}.{COMPANY}.com'
                    ],
                    'path_matcher': 'allpaths'
                }],
                'name': name,
                'path_matcher': [{
                    'default_service': (
                        '${google_compute_backend_service.'
                        f'{default_version}.id}}'
                    ),
                    'name': 'allpaths',
                    'path_rule': [{
                        'paths': [
                            '/*'
                        ],
                        'route_action': {
                            'weighted_backend_services':
                                _generate_backend_services(
                                    services)
                        }
                    }]
                }]
            }]
        }
    }]
