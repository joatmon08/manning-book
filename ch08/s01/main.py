import json
import iam


def build_frontend_configuration():
    name = 'frontend'
    roles = [
        'roles/compute.networkAdmin',
        'roles/appengine.appAdmin',
        'roles/cloudsql.admin'
    ]

    frontend = iam.ApplicationFactoryModule(name, roles)
    resources = {
        'resource': frontend._build()
    }
    return resources


if __name__ == "__main__":
    resources = build_frontend_configuration()

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile, sort_keys=True, indent=4)
