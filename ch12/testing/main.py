import json
import sys


sys.path.insert(1, '../modules')
import schedule
import server


ENVIRONMENT = 'testing'
REGION = 'us-central1'
ZONE = 'us-central1-a'

## In the text, I use n2d machine types. They
## can be quite expensive and have a quota
## on the platform. You can uncomment
## the code to use `e2-micro` instances.
# MACHINE_TYPE = 'e2-micro'
MACHINE_TYPE = 'n2d-standard-8'


if __name__ == "__main__":
    data, resources = schedule.iam()
    resources.append(schedule.build(
        f'{ENVIRONMENT}-schedule',
        REGION, '2021-12-03'))
    for i in range(0, 2):
        resources.append(server.build(
            f'{ENVIRONMENT}-server-{i}',
            MACHINE_TYPE, ZONE))
    config = {
        'data': data,
        'resource': resources
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile,
                  sort_keys=True, indent=4)
