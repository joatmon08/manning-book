import re

TEAM = 'sundew'
ENVIRONMENT = 'production'
VERSION = 'blue'
REGION = 'us-central1'
IP_RANGE = '10.0.0.0/24'
EMAIL_DOMAIN = f'{TEAM}.com'

users = {
    f'group:audit-team@{EMAIL_DOMAIN}': 'roles/viewer',
    f'automation-watering@{EMAIL_DOMAIN}': 'roles/editor',
    f'user-02@{EMAIL_DOMAIN}': 'roles/owner'
}


def build():
    return iam()


def iam(users=users):
    iam_members = []
    for user, role in users.items():
        user_id = re.sub("[^0-9a-zA-Z]+", "_", user)
        iam_members.append({
            'google_project_iam_member': [{
                user_id: [{
                    'role': role,
                    'member': user
                }]
            }]
        })
    return iam_members
