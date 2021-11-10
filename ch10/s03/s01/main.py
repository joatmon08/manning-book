import blue
import iam
import json
import os

if __name__ == "__main__":
    resources = {
        'resource': blue.build()
        + iam.build()
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
