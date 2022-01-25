import json
from server import DatabaseServerFactory
from loadbalancer import LoadBalancerFactory
from firewall import FirewallFactory


class DatabaseModule:
    def __init__(self, name):
        self._resources = []
        self._name = name
        self._resources = DatabaseServerFactory(
            self._name).resources

    def add_internal_load_balancer(self):
        self._resources.extend(
            LoadBalancerFactory(
                self._name, external=False).resources)

    def add_external_load_balancer(self):
        self._resources.extend(
            LoadBalancerFactory(
                self._name, external=True).resources)

    def add_google_firewall_rule(self):
        self._resources.extend(
            FirewallFactory(
                self._name).resources)

    def build(self):
        return {
            'resource': self._resources
        }


if __name__ == "__main__":
    database_module = DatabaseModule('development-database')
    database_module.add_external_load_balancer()
    database_module.add_google_firewall_rule()

    with open('main.tf.json', 'w') as outfile:
        json.dump(database_module.build(), outfile,
                  sort_keys=True, indent=4)
