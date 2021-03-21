import json
import re


class StorageBucketFacade:
    def __init__(self, name):
        self.name = name


class StorageBucketModule:
    def __init__(self, name, location='US'):
        self.name = f'{name}-storage-bucket'
        self.location = location
        self.resources = self._build()

    def _build(self):
        return {
            'resource': [
                {
                    'google_storage_bucket': [{
                        self.name: [{
                            'name': self.name,
                            'location': self.location,
                            'force_destroy': True
                        }]
                    }]
                }
            ]
        }

    def outputs(self):
        return StorageBucketFacade(self.name)


class StorageBucketAccessModule:
    def __init__(self, bucket, user, role):
        if not self._validate_user(user):
            print("Please enter valid user or group ID")
            exit()
        if not self._validate_role(role):
            print("Please enter valid role")
            exit()
        self.bucket = bucket
        self.user = user
        self.role = role
        self.resources = self._build()

    def _validate_role(self, role):
        valid_roles = ['READER', 'OWNER', 'WRITER']
        if role in valid_roles:
            return True
        return False

    def _validate_user(self, user):
        valid_users_group = ['allUsers', 'allAuthenticatedUsers']
        if user in valid_users_group:
            return True
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, user)):
            return True
        return False

    def _change_case(self):
        return re.sub('[^0-9a-zA-Z]+', '_', self.user)

    def _build(self):
        return {
            'resource': [{
                'google_storage_bucket_access_control': [{
                    self._change_case(): [{
                        'bucket': self.bucket.name,
                        'role': self.role,
                        'entity': self.user
                    }]
                }]
            }]
        }


if __name__ == "__main__":
    bucket = StorageBucketModule('hello-world')
    with open('bucket.tf.json', 'w') as outfile:
        json.dump(bucket.resources, outfile, sort_keys=True, indent=4)

    server = StorageBucketAccessModule(
        bucket.outputs(), 'allAuthenticatedUsers', 'READER')
    with open('bucket_access.tf.json', 'w') as outfile:
        json.dump(server.resources, outfile, sort_keys=True, indent=4)
