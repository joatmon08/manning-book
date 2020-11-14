import json
import os


def google_project_for_reporting_application():
    name = 'report-application'  #A
    organization = os.environ.get('USER')  #B
    project_id = f'{name}-{organization}'  #B
    return {
        'resource': [
            {
                'google_project': [
                    {
                        'reporting_application': [
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
    config = google_project_for_reporting_application()  #C

    with open('main.tf.json', 'w') as outfile:  #D
        json.dump(config, outfile, sort_keys=True, indent=4)  #D
