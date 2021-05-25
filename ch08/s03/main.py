from firewall import FirewallFactoryModule
from database import DatabaseFactoryModule

import json

environment = 'development'
APP_NAME = f'{environment}-frontend-database'
CONFIGURATION_FILE = 'main.tf.json'


def build_frontend_configuration():

    firewall = FirewallFactoryModule(
        APP_NAME,
        ports=[1433],
        allow_cidr_blocks=['0.0.0.0/0']
    )
    database = DatabaseFactoryModule(APP_NAME)
    return {
        'resource': firewall.build() + database.build()
    }


if __name__ == "__main__":
    with open(CONFIGURATION_FILE, 'w') as outfile:
        json.dump(build_frontend_configuration(),
                  outfile, sort_keys=True, indent=4)
