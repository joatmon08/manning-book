import json
import sys


sys.path.insert(1, '../modules')
import server


ENVIRONMENT = 'prod'
ZONE = 'us-central1-a'

if __name__ == "__main__":
    resources = []
    resources.append(server.build(
        f'{ENVIRONMENT}-server-conf-0',
        'n2d-standard-16', ZONE))
    resources.append(server.build(
        f'{ENVIRONMENT}-server-conf-1',
        'n2d-standard-16', ZONE))
    resources.append(server.build(
        f'{ENVIRONMENT}-server-0',
        'n2d-standard-32', ZONE))
    resources.append(server.build(
        f'{ENVIRONMENT}-server-1',
        'n2d-standard-32', ZONE))
    resources.append(server.build(
        f'{ENVIRONMENT}-server-2',
        'n2d-standard-32', ZONE))
    config = {
        'resource': resources
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile,
                  sort_keys=True, indent=4)
