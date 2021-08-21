TEAM = 'sundew'
ENVIRONMENT = 'production'
VERSION = 'blue'
REGION = 'us-central1'
IP_RANGE = '10.0.0.0/24'

zone = f'{REGION}-a'
network_name = f'{TEAM}-{ENVIRONMENT}-network-{VERSION}'

cluster_name = f'{TEAM}-{ENVIRONMENT}-cluster-{VERSION}'
cluster_nodes = f'{TEAM}-{ENVIRONMENT}-cluster-nodes-{VERSION}'
cluster_service_account = f'{TEAM}-{ENVIRONMENT}-sa-{VERSION}'

labels = {
    'team': TEAM,
    'environment': ENVIRONMENT,
    'automated': True
}


def build():
    return network() + \
        cluster()


def network(name=network_name,
            region=REGION,
            ip_range=IP_RANGE):
    return [
        {
            'google_compute_network': {
                VERSION: [{
                    'name': name,
                    'auto_create_subnetworks': False
                }]
            }
        },
        {
            'google_compute_subnetwork': {
                VERSION: [{
                    'name': f'{name}-subnet',
                    'region': region,
                    'network': f'${{google_compute_network.{VERSION}.name}}',
                    'ip_cidr_range': ip_range
                }]
            }
        }
    ]


def cluster(name=cluster_name,
            node_name=cluster_nodes,
            service_account=cluster_service_account,
            region=REGION):
    return [
        {
            'google_container_cluster': {
                VERSION: [
                    {
                        'initial_node_count': 1,
                        'location': region,
                        'name': name,
                        'remove_default_node_pool': True,
                        'network': f'${{google_compute_network.{VERSION}.name}}',
                        'subnetwork': f'${{google_compute_subnetwork.{VERSION}.name}}'
                    }
                ]
            },
            'google_container_node_pool': {
                VERSION: [
                    {
                        'cluster': f'${{google_container_cluster.{VERSION}.name}}',
                        'location': region,
                        'name': node_name,
                        'node_config': [
                            {
                                'machine_type': 'e2-micro',
                                'oauth_scopes': [
                                    'https://www.googleapis.com/auth/cloud-platform'
                                ],
                                'preemptible': True,
                                'service_account': f'${{google_service_account.{VERSION}.email}}'
                            }
                        ],
                        'node_count': 0
                    }
                ]
            },
            'google_service_account': {
                VERSION: [
                    {
                        'account_id': service_account,
                        'display_name': service_account
                    }
                ]
            }
        }
    ]