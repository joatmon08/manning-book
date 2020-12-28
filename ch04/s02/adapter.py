class Network:
    def __init__(self, network, cidr_block):
        self._network = network
        self._cidr_block = cidr_block

class NetworkFactory:
    def __init__(self, name, ip_range, subnet_ip_range):
        self._network_name = f'{name}-network'
        self._subnet_name = f'{name}-subnet'
        self._vpn_name = f'{name}-vpn'
        self._ip_range = ip_range
        self._subnet_ip_range = subnet_ip_range