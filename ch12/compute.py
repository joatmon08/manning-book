import googleapiclient.discovery
import re


class MachineType():
    def __init__(self, gcp_json):
        self.name = gcp_json['name']
        self.description = gcp_json['description']
        self.cpus, self.ram = self._parse_cpu_and_ram()
        self.maxPersistentDisks = gcp_json[
            'maximumPersistentDisks']
        self.maxPersistentDiskSizeGb = gcp_json[
            'maximumPersistentDisksSizeGb']
        self.isSharedCpu = gcp_json['isSharedCpu']

    def _parse_cpu_and_ram(self):
        result = re.search(
            f"([0-9]+) vCPUs ([0-9]+) GB RAM",
            self.description)
        cpu, ram = result.groups()
        return int(cpu), int(ram)


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
