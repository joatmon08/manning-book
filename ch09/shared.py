TEAM = 'sundew'
ENVIRONMENT = 'production'

load_balancer_name = f'{TEAM}-{ENVIRONMENT}-forwarding-rule'

def load_balancer(name=load_balancer_name,
            region=REGION,
            ip_range=IP_RANGE):
    return [
        {
            'google_compute_forwarding_rule': {
                'blue': [{
                    'all_ports': True,
                    'backend_service': '${google_compute_region_backend_service.backend.id}',
                    'load_balancing_scheme': 'INTERNAL',
                    'name': name,
                    'network': '${google_compute_network.network_blue.name}',
                    'region': region,
                    'subnetwork': '${google_compute_subnetwork.subnet_blue.name}'
                }]
            }
        },
        {
            'google_compute_subnetwork': {
                'subnet': [{
                    'name': f'{name}-subnet',
                    'region': region,
                    'network': '${google_compute_network.network.name}',
                    'ip_cidr_range': ip_range
                }]
            }
        }
    ]