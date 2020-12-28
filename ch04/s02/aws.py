import adapter


class Network(adapter.NetworkFactory):
    def __init__(self, name, ip_range, subnet_ip_range, peer):
        adapter.NetworkFactory.__init__(self, name, ip_range, subnet_ip_range)
        self.peer = peer
        self.resources = self._build()

    def _build(self):
        return {
            'resource': [
                {
                    'aws_vpc': [{
                        self._network_name: [{
                            'name': self._network_name,
                            'cidr_block': self._ip_range,
                            'enable_dns_support': True,
                            'enable_dns_hostnames': True
                        }]
                    }]
                },
                {
                    'aws_subnet': [{
                        self._network_name: [{
                            'vpc_id': f'${{aws_vpc.aws.{self._network_name}}}',
                            'cidr_block': self._ip_range
                        }]
                    }]
                },
                {
                    'aws_internet_gateway': [{
                        self._network_name: [{
                            'vpc_id': f'${{aws_vpc.aws.{self._network_name}}}'
                        }]
                    }]
                },
                {
                    'aws_vpn_gateway': [{
                        self._vpn_name: [{
                            'vpc_id': f'${{aws_vpc.aws.{self._network_name}}}'
                        }]
                    }]
                },
                {
                    'aws_customer_gateway': [{
                        self._vpn_name: [{
                            'bgp_asn': 65000,
                            'type': "ipsec.1",
                            'ip_address': self.peer._cidr_block
                        }]
                    }]
                },
                {
                    'aws_vpn_connection': [{
                        self._vpn_name: [{
                            'vpn_gateway_id': '${aws_vpn_gateway.aws-vpn-gw.id}',
                            'customer_gateway_id': '${aws_customer_gateway.aws-cgw.id}',
                            'static_routes_only': False,
                            'type': "ipsec.1"
                        }]
                    }]
                }
            ]
        }

    def outputs(self):
        return adapter.Network(self._subnet_name, self._ip_range)
