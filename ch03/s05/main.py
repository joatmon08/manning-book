import json
from server import google_db_server_group
from loadbalancer import google_load_balancer
from firewall import google_firewall_rule


class DatabaseModule:
    def __init__(self, name) -> None:
        self._resources = []
        self._name = name
        google_db_server_group(self._resources, self._name)

    def add_internal_load_balancer(self):
        google_load_balancer(self._resources, self._name)

    def add_external_load_balancer(self):
        google_load_balancer(self._resources, self._name, external=True)

    def add_google_firewall_rule(self):
        google_firewall_rule(self._resources, self._name)

    def build(self):
        return {
            'resource': self._resources
        }


if __name__ == "__main__":

    database_module = DatabaseModule('hello-world')
    database_module.add_external_load_balancer()
    database_module.add_google_firewall_rule()

    with open('main.tf.json', 'w') as outfile:
        json.dump(database_module.build(), outfile, sort_keys=True, indent=4)
