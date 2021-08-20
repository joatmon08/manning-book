TEAM = 'sundew'

users = {
    'audit-team': 'roles/viewer',
    'automation-watering': 'roles/editor',
    'user-02': 'roles/owner'
}


def build():
    return iam()


def iam(users=users):
    iam_members = []
    for user, role in users.items():
        user_id = user.replace('-', '_')
        iam_members.append({
            'google_service_account': [{
                user_id: [{
                    'account_id': user,
                    'display_name': user
                }]
            }]
        })
        iam_members.append({
            'google_project_iam_member': [{
                user_id: [{
                    'role': role,
                    'member': 'serviceAccount:${google_service_account.'
                    + f'{user_id}' + '.email}'
                }]
            }]
        })
    return iam_members
