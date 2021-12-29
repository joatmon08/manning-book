from tags import StandardTags
from server import ServerFactoryModule
from network import NetworkFactoryModule
from database import DatabaseFactoryModule

import json

if __name__ == "__main__":
    environment = 'production'
    name = f'{environment}-hello-world'

    tags = StandardTags(environment)
    network = NetworkFactoryModule(name)
    server = ServerFactoryModule(name, environment, network, tags.tags)
    database = DatabaseFactoryModule(
        name, server, network, environment, tags.tags)
    resources = {
        'resource': network.build() + server.build() + database.build()
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile, sort_keys=True, indent=4)
