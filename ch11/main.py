import os
import database
import iam
import network
import server
import json
import os

SERVICE = 'promotions'
ENVIRONMENT = 'prod'
REGION = 'us-central1'
ZONE = 'us-central1-a'
PROJECT = os.environ['CLOUDSDK_CORE_PROJECT']
role = 'roles/cloudsql.client'

if __name__ == "__main__":
    resources = {
        'resource':
        network.Module(SERVICE, ENVIRONMENT, REGION).build() +
        iam.Module(SERVICE, ENVIRONMENT, REGION, PROJECT,
                   role).build() +
        database.Module(SERVICE, ENVIRONMENT, REGION).build() +
        server.Module(SERVICE, ENVIRONMENT, ZONE).build()
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
