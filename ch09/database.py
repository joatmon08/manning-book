import random
import string

TEAM = 'sundew'
ENVIRONMENT = 'production'
VERSION = 'blue'
REGION = 'us-central1'

zone = f'{REGION}-a'

name = f'{TEAM}-{ENVIRONMENT}-database-{VERSION}'

labels = {
    'team': TEAM,
    'environment': ENVIRONMENT,
    'automated': True
}


def build():
    return network() + database()


def network(name=name):
    return [{
        'google_compute_global_address': {
            VERSION: [{
                'address_type': 'INTERNAL',
                'name': name,
                'network': f'${{google_compute_network.{VERSION}.id}}',
                'prefix_length': 24,
                'provider': 'google-beta',
                'purpose': 'VPC_PEERING'
            }]
        },
        'google_service_networking_connection': {
            VERSION: [{
                'network': f'${{google_compute_network.{VERSION}.id}}',
                'provider': 'google-beta',
                'reserved_peering_ranges': [
                    f'${{google_compute_global_address.{VERSION}.name}}'
                ],
                'service': 'servicenetworking.googleapis.com'
            }]
        }
    }]


def database(name=name):
    suffix = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits)
        for i in range(4))
    return [{
        'google_sql_database_instance': {
            VERSION: [{
                'depends_on': [f'google_service_networking_connection.{VERSION}'],
                'deletion_protection': False,
                'region': REGION,
                'database_version': 'POSTGRES_12',
                'name': f'{name}-suffix',
                'settings': [{
                    'ip_configuration': [{
                        'private_network':
                        f'${{google_compute_network.{VERSION}.id}}'
                    }],
                    'tier': 'db-f1-micro',
                    'user_labels': labels,
                    'location_preference': {
                        'zone': zone
                    }
                }]
            }]
        }
    }]


