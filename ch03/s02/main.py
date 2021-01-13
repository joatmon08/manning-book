import json
import os


class DatabaseGoogleProject:
    def __init__(self):
        self.name = 'databases'  # A
        self.organization = os.environ.get('USER')  # B
        self.project_id = f'{self.name}-{self.organization}'  # B
        self.resource = self._build()

    def _build(self):
        return {
            'resource': [
                {
                    'google_project': [
                        {
                            'databases': [
                                {
                                    'name': self.name,
                                    'project_id': self.project_id
                                }
                            ]
                        }
                    ]
                }
            ]
        }


if __name__ == "__main__":
    project = DatabaseGoogleProject()  # C

    with open('main.tf.json', 'w') as outfile:  # D
        json.dump(project.resource, outfile, sort_keys=True, indent=4)  # D
