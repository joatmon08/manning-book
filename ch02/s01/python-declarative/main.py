import json

def hello_server(name):
    return {
        'resource': [
            {
                'google_compute_instance': [
                    {
                        name: [
                            {
                                'allow_stopping_for_update': True,
                                'boot_disk': [
                                    {
                                        'initialize_params': [
                                            {
                                                'image': 'ubuntu-1804-lts'
                                            }
                                        ]
                                    }
                                ],
                                'machine_type': 'f1-micro',
                                'name': name,
                                'network_interface': [
                                    {
                                        'network': 'default'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


if __name__ == "__main__":
    servers = ['hello-world', 'hello-world-2']
    for server in servers:
        config = hello_server(name=server)

        with open(server + '.tf.json', 'w') as outfile:
            json.dump(config, outfile, sort_keys=True, indent=4)
