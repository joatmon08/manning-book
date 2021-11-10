from datetime import datetime, timezone
import os

project = os.environ['CLOUDSDK_CORE_PROJECT']


def iam():
    compute_service_account = \
        'service-${data.google_project.project.number}' + \
        '@compute-system.iam.gserviceaccount.com'
    data = [{
        'google_project': {
            'project': {}
        }
    }]
    resources = [{
        'google_project_iam_custom_role': {
            'weekend': {
                'role_id': 'weekendShutdown',
                'title': 'Weekend Shutdown of Servers',
                'permissions': [
                    'compute.instances.start',
                    'compute.instances.stop'
                ]
            }
        }
    }, {
        'google_project_iam_binding': {
            'weekend': {
                'role': '${google_project_iam_custom_role' +
                '.weekend.id}',
                'members': [
                    f'serviceAccount:{compute_service_account}'
                ],
                'project': project
            }
        }
    }]
    return data, resources


def build(name, region, week_before_conference):
    expiration_time = datetime.strptime(
        week_before_conference,
        '%Y-%m-%d').replace(
            tzinfo=timezone.utc).isoformat().replace(
                '+00:00', 'Z')
    return {
        'google_compute_resource_policy': {
            'weekend': {
                'name': name,
                'region': region,
                'description':
                'start and stop instances over the weekend',
                'instance_schedule_policy': {
                    'vm_start_schedule': {
                        'schedule': '0 0 * * MON'
                    },
                    'vm_stop_schedule': {
                        'schedule': '0 0 * * SAT'
                    },
                    'time_zone': 'US/Central',
                    'expiration_time': expiration_time
                }
            }
        }
    }


def id():
    return '${google_compute_resource_policy.weekend.id}'


def service_account():
    return '${google_service_account.weekend.email}'
