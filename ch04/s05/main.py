import json
from server import ServerFactoryModule
from firewall import FirewallFactoryModule
from network import NetworkFactoryModule


class Mediator:
    def __init__(self, resource, **attributes):
        self.resources = self._create(resource, **attributes)

    def _create(self, resource, **attributes):
        if isinstance(resource, FirewallFactoryModule):
            server = ServerFactoryModule(resource._name)
            resources = self._create(server)
            firewall = FirewallFactoryModule(
                resource._name, depends_on=resources[1].outputs())
            resources.append(firewall)
        elif isinstance(resource, ServerFactoryModule):
            network = NetworkFactoryModule(resource._name)
            resources = self._create(network)
            server = ServerFactoryModule(
                resource._name, depends_on=network.outputs())
            resources.append(server)
        else:
            resources = [resource]
        return resources

    def build(self):
        metadata = []
        for resource in self.resources:
            metadata += resource.build()
        return {'resource': metadata}


if __name__ == "__main__":
    name = 'hello-world'
    resource = FirewallFactoryModule(name)
    # Uncomment to create network only
    # resource = NetworkFactoryModule(name, ip_range='10.0.0.0/16')
    # Uncomment to create server and network only
    # resource = ServerFactoryModule(name)
    mediator = Mediator(resource)

    with open('main.tf.json', 'w') as outfile:
        json.dump(mediator.build(), outfile, sort_keys=True, indent=4)
