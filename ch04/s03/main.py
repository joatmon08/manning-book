import json
from server import ServerFactoryModule
from network import NetworkFactoryModule


class Mediator:
    def __init__(self, resource, **attributes):
        self.resources = self._create(resource, **attributes)

    def _create(self, resource, **attributes):
        if isinstance(resource, ServerFactoryModule):
            network = NetworkFactoryModule(resource._name)
            resources = self._create(network)
            server = ServerFactoryModule(
                resource._name, network._network_name)
            resources += server._build()
        else:
            resources = resource._build()
        return resources

    def build(self):
        return {'resource': self.resources}


if __name__ == "__main__":
    name = 'hello-world'
    resource = ServerFactoryModule(name)
    # Uncomment to create network only
    # resource = NetworkFactoryModule(name, ip_range='10.0.0.0/16')
    mediator = Mediator(resource)

    with open('main.tf.json', 'w') as outfile:
        json.dump(mediator.build(), outfile, sort_keys=True, indent=4)
