
import json
from modules import server


ENVIRONMENT = 'testing'
ZONE = 'us-central1-a'

MACHINE_TYPE_SANDBOX = 'e2-micro'

if __name__ == "__main__":
    config = {
        'resource': [
            server.build(
                f'{ENVIRONMENT}-server-sandbox-0',
                ENVIRONMENT, MACHINE_TYPE_SANDBOX, ZONE,
                long_term=False),
            server.build(
                f'{ENVIRONMENT}-server-0',
                ENVIRONMENT, MACHINE_TYPE_SANDBOX, ZONE,
                long_term=True),
        ]
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile,
                  sort_keys=True, indent=4)
