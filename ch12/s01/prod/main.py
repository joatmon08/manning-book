import json
import sys


sys.path.insert(1, '../modules')
import schedule
import server


ENVIRONMENT = 'prod'
REGION = 'us-central1'
ZONE = 'us-central1-a'

## In the text, I use n2d machine types. They
## can be quite expensive and have a quota
## on the platform. You can uncomment
## the code to use `e2-micro` instances.
# MACHINE_TYPE_SANDBOX = 'e2-micro'
# MACHINE_TYPE_PROD = 'e2-micro'
MACHINE_TYPE_SANDBOX = 'n2d-standard-16'
MACHINE_TYPE_PROD = 'n2d-standard-32'

if __name__ == "__main__":
    resources = []
    resources.append(schedule.build(
        f'{ENVIRONMENT}-schedule',
        REGION, '2021-12-03'))
    for i in range(0, 2):
        resources.append(server.build(
            f'{ENVIRONMENT}-server-sandbox-{i}',
            MACHINE_TYPE_SANDBOX, ZONE))
    for i in range(0, 3):
        resources.append(server.build(
            f'{ENVIRONMENT}-server-{i}',
            MACHINE_TYPE_PROD, ZONE))
    config = {
        'resource': resources
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile,
                  sort_keys=True, indent=4)
