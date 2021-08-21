import iam
import os
import googleapiclient.discovery
import subprocess

PROJECT = os.environ['CLOUDSDK_CORE_PROJECT']


def _get_members_from_gcp(project, roles):
    roles_and_members = {}
    service = googleapiclient.discovery.build(
        'cloudresourcemanager', 'v1')
    result = service.projects().getIamPolicy(
        resource=project, body={}).execute()
    bindings = result['bindings']
    for binding in bindings:
        if binding['role'] in roles:
            roles_and_members[binding['role']] = binding['members']
    return roles_and_members


def _set_emails_and_roles(users, all_members):
    members = []
    for username, role in users.items():
        members += [(iam.get_user_id(username), m, role)
                    for m in all_members[role] if username in m]
    return members


def check_import_status(ret, err):
    return ret != 0 and \
        'Resource already managed by Terraform' not in str(err)


def import_service_account(project_id, user_id, user_email):
    email = user_email.replace('serviceAccount:', '')
    command = ['terraform', 'import', '-no-color',
               f'{iam.TERRAFORM_GCP_SERVICE_ACCOUNT_TYPE}.{user_id}',
               f'projects/{project_id}/serviceAccounts/{email}']
    return _terraform(command)


def import_project_iam_member(project_id, role,
                              user_id, user_email):
    command = ['terraform', 'import', '-no-color',
               f'{iam.TERRAFORM_GCP_ROLE_ASSIGNMENT_TYPE}.{user_id}',
               f'{project_id} {role} {user_email}']
    return _terraform(command)


def _terraform(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


if __name__ == "__main__":
    sundew_iam = iam.users
    all_members_for_roles = _get_members_from_gcp(
        PROJECT, set(sundew_iam.values()))
    import_members = _set_emails_and_roles(
        sundew_iam, all_members_for_roles)
    for user_id, email, role in import_members:
        ret, _, err = import_service_account(PROJECT,
                                             user_id, email)
        if check_import_status(ret, err):
            print(f'import service account failed: {err}')
        ret, _, err = import_project_iam_member(PROJECT, role,
                                                user_id, email)
        if check_import_status(ret, err):
            print(f'import iam member failed: {err}')
