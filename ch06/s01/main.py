import json
import os
import version

SERVICE_CONFIGURATION_FILE = 'main.tf.json'
SERVICE_IMAGE = 'us-docker.pkg.dev/cloudrun/container/hello'
SERVICE_NAME = 'hello-world'


class GoogleCloudRunFactoryModule:
    def __init__(self, name, image, version,
                 location='us-central1'):
        self._name = name
        self._location = location
        self._image = f'{image}@{version}'
        self.resources = self._build()

    def _build(self):
        service = f"${{google_cloud_run_service.{self._name}.name}}"
        location = f"${{google_cloud_run_service.{self._name}.location}}"
        url = f"${{google_cloud_run_service.{self._name}.status[0].url}}"

        return {
            'resource': [{
                'google_cloud_run_service': [{
                    self._name: [{
                        'name': self._name,
                        'location': self._location,
                        'template': {
                            'spec': {
                                'containers': {
                                    'image': self._image
                                }
                            }
                        },
                        'traffic': {
                            'percent': 100,
                            'latest_revision': True
                        }
                    }]
                }],
                'google_cloud_run_service_iam_member': [{
                    self._name: [{
                        'service': service,
                        'location': location,
                        'role': 'roles/run.invoker',
                        'member': 'allUsers'
                    }]
                }]
            }],
            'output': {
                'url': {
                    'value': url
                }
            }
        }


def generate_json(service_name):
    service = GoogleCloudRunFactoryModule(
        name=service_name,
        image=SERVICE_IMAGE,
        version=version.HELLO
    )
    with open(SERVICE_CONFIGURATION_FILE, 'w') as outfile:
        json.dump(service.resources, outfile,
                  sort_keys=True, indent=4)
