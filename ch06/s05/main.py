import json

SERVICE_CONFIGURATION_FILE = 'main.tf.json'


class GoogleCloudRunFactoryModule:
    def __init__(self, name,
                 location='us-central1',
                 image='us-docker.pkg.dev/cloudrun/container/hello'):
        self._name = name
        self._location = location
        self._image = image
        self.resources = self._build()

    def _build(self):
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
                        'service': f"${{google_cloud_run_service.{self._name}.name}}",
                        'location': f"${{google_cloud_run_service.{self._name}.location}}",
                        'role': 'roles/run.invoker',
                        'member': 'allUsers'
                    }]
                }]
            }],
            'output': {
                'url': {
                    'value': f"${{google_cloud_run_service.{self._name}.status[0].url}}"
                }
            }
        }


def generate_json(service_name):
    service = GoogleCloudRunFactoryModule(
        name=service_name
    )
    with open(SERVICE_CONFIGURATION_FILE, 'w') as outfile:
        json.dump(service.resources, outfile,
                  sort_keys=True, indent=4)
