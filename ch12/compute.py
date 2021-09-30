import googleapiclient.discovery


class MachineType():
    def __init__(self, gcp_json):
        self.name = gcp_json['name']
        self.cpus = gcp_json['guestCpus']
        self.memoryMb = gcp_json['memoryMb']
        self.maxPersistentDisks = gcp_json[
            'maximumPersistentDisks']
        self.maxPersistentDiskSizeGb = gcp_json[
            'maximumPersistentDisksSizeGb']
        self.isSharedCpu = gcp_json['isSharedCpu']


def get_machine_type(project, zone, type):
    service = googleapiclient.discovery.build(
        'compute', 'v1')
    result = service.machineTypes().list(
        project=project,
        zone=zone,
        filter=f'name:"{type}"').execute()
    types = result['items'] if 'items' in result else None
    if len(types) != 1:
        return None
    return MachineType(types[0])
