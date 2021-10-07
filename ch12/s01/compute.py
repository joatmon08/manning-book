import googleapiclient.discovery


class MachineType():
    def __init__(self, gcp_json):
        self.name = gcp_json['name']
        self.description = gcp_json['description']
        self.cpus = gcp_json['guestCpus']
        self.ram = self._convert_mb_to_gb(
            gcp_json['memoryMb'])
        self.maxPersistentDisks = gcp_json[
            'maximumPersistentDisks']
        self.maxPersistentDiskSizeGb = gcp_json[
            'maximumPersistentDisksSizeGb']
        self.isSharedCpu = gcp_json['isSharedCpu']

    def _convert_mb_to_gb(self, mb):
        GIGABYTE = 1.0/1024
        return GIGABYTE * mb


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
