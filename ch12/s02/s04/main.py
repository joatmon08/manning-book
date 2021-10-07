import json
from modules import instance_group


ENVIRONMENT = 'prod'
REGION = 'us-central1'
ZONE = 'us-central1-a'

# In the text, I use n2d machine types. They
# can be quite expensive and have a quota
# on the platform. You can uncomment
# the code to use `e2-micro` instances.
MACHINE_TYPE = 'e2-micro'
# MACHINE_TYPE = 'n2d-standard-32'


if __name__ == "__main__":
    resources = instance_group.build(
        ENVIRONMENT, MACHINE_TYPE, ZONE,
        1, 3, 0.75
    )
    config = {
        'resource': resources
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile,
                  sort_keys=True, indent=4)
