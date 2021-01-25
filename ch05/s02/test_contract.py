from network import NetworkFactoryModule


def test_network_outputs_contains_name_and_ip_address_for_server():
    network_name = 'hello-world'
    network_cidr_range = '10.0.0.0/16'
    network = NetworkFactoryModule(
        name=network_name, ip_range=network_cidr_range)

    assert network.outputs()._network == f"{network_name}-subnet"
    assert network.outputs()._ip_cidr_range == network_cidr_range
