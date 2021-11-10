import os

TEAM = 'sundew'
TERRAFORM_GCP_SERVICE_ACCOUNT_TYPE = 'google_service_account'
TERRAFORM_GCP_ROLE_ASSIGNMENT_TYPE = 'google_project_iam_member'

users = {
    'audit-team': 'roles/viewer',
    'automation-watering': 'roles/editor',
    'user-02': 'roles/owner'
}

project = os.environ['CLOUDSDK_CORE_PROJECT']


def get_user_id(user):
    return user.replace('-', '_')


def build():
    return iam()


def iam(users=users):
    iam_members = []
    for user, role in users.items():
        user_id = get_user_id(user)
        iam_members.append({
            TERRAFORM_GCP_SERVICE_ACCOUNT_TYPE: [{
                user_id: [{
                    'account_id': user,
                    'display_name': user
                }]
            }]
        })
        iam_members.append({
            TERRAFORM_GCP_ROLE_ASSIGNMENT_TYPE: [{
                user_id: [{
                    'role': role,
                    'member': 'serviceAccount:${google_service_account.'
                    + f'{user_id}' + '.email}',
                    'project': project
                }]
            }]
        })
    return iam_members
