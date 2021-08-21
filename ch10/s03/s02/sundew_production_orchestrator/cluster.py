import googleapiclient.discovery
import os

PROJECT = os.environ['CLOUDSDK_CORE_PROJECT']
TEAM = 'sundew'
ENVIRONMENT = 'production'
VERSION = 'blue'
REGION = 'us-central1'

cluster_name = f'{TEAM}-{ENVIRONMENT}-cluster-{VERSION}'
cluster_nodes = f'{TEAM}-{ENVIRONMENT}-cluster-nodes-{VERSION}'
cluster_service_account = f'{TEAM}-{ENVIRONMENT}-sa-{VERSION}'


def _get_network_from_gcp():
    service = googleapiclient.discovery.build(
        'compute', 'v1')
    result = service.subnetworks().list(
        project=PROJECT,
        region=REGION,
        filter=f'name:"{TEAM}-{ENVIRONMENT}-*"').execute()
    subnetworks = result['items'] if 'items' in result else None
    if len(subnetworks) != 1:
        print("Network not found")
        exit(1)
    return subnetworks[0]['network'].split('/')[-1], \
        subnetworks[0]['name']


def build():
    return cluster()


def cluster(name=cluster_name,
            node_name=cluster_nodes,
            service_account=cluster_service_account,
            region=REGION):
    network, subnet = _get_network_from_gcp()
    return [
        {
            'google_container_cluster': {
                VERSION: [
                    {
                        'initial_node_count': 1,
                        'location': region,
                        'name': name,
                        'remove_default_node_pool': True,
                        'network': network,
                        'subnetwork': subnet
                    }
                ]
            },
            'google_container_node_pool': {
                VERSION: [
                    {
                        'cluster':
                        '${google_container_cluster.' +
                            f'{VERSION}' + '.name}',
                        'location': region,
                        'name': node_name,
                        'node_config': [
                            {
                                'machine_type': 'e2-micro',
                                'oauth_scopes': [
                                    'https://www.googleapis.com/' +
                                    'auth/cloud-platform'
                                ],
                                'preemptible': True,
                                'service_account':
                                '${google_service_account.' +
                                    f'{VERSION}' + '.email}'
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
