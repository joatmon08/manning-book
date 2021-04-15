import sys
sys.path.insert(1, '../../modules/gcp')

# import server and network modules
from database import DatabaseFactoryModule
from server import ServerFactoryModule
from network import NetworkFactoryModule

import json


if __name__ == "__main__":
    environment = 'production'
    name = f'{environment}-hello-world'
    network = NetworkFactoryModule(name)
    server = ServerFactoryModule(name, environment, network)
    database = DatabaseFactoryModule(name, server, network, environment)
    resources = {
        'resource': network.build() + server.build() + database.build()
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile, sort_keys=True, indent=4)
