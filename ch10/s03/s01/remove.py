from sundew_production_iam import iam
import subprocess


def check_state_remove_status(ret, err):
    return ret != 0 \
        and 'No matching objects found' not in str(err)


def state_remove(resource_type, resource_identifier):
    command = ['terraform', 'state', 'rm', '-no-color',
               f'{resource_type}.{resource_identifier}']
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
    for user in iam.users:
        ret, _, err = state_remove(
            iam.TERRAFORM_GCP_SERVICE_ACCOUNT_TYPE,
            iam.get_user_id(user))
        if check_state_remove_status(ret, err):
            print(f'remove service account from state failed: {err}')
        ret, _, err = state_remove(
            iam.TERRAFORM_GCP_ROLE_ASSIGNMENT_TYPE,
            iam.get_user_id(user))
        if check_state_remove_status(ret, err):
            print(f'remove role assignment from state failed: {err}')
