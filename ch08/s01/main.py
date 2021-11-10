import json
import iam
import os


def build_frontend_configuration():
    name = 'frontend'
    roles = [
        'roles/compute.networkAdmin',
        'roles/appengine.appAdmin',
        'roles/cloudsql.admin'
    ]
    project = os.environ['CLOUDSDK_CORE_PROJECT']

    frontend = iam.ApplicationFactoryModule(name, roles, project)
    resources = {
        'resource': frontend._build()
    }
    return resources


if __name__ == "__main__":
    resources = build_frontend_configuration()

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile, sort_keys=True, indent=4)
