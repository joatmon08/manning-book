import json
import os

def google_project_for_databases():
    name = 'databases'  # A
    organization = os.environ.get('USER')  # B
    project_id = f'{name}-{organization}'  # B
    return {
        'resource': [
            {
                'google_project': [
                    {
                        'databases': [
                            {
                                'name': name,
                                'project_id': project_id
                            }
                        ]
                    }
                ]
            }
        ]
    }


if __name__ == "__main__":
    config = google_project_for_databases()  # C

    with open('main.tf.json', 'w') as outfile:  # D
        json.dump(config, outfile, sort_keys=True, indent=4)  # D
