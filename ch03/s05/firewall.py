def google_firewall_rule(resources, name, network='default'):
    resources.append({
        'google_compute_firewall': [{
            'db': [
                {
                    'allow': [
                        {
                            'protocol': 'tcp',
                            'ports': ['3306']
                        }
                    ],
                    'name': name,
                    'network': network
                }
            ]
        }
        ]
    })
