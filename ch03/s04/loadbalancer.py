def google_load_balancer(resources, name, region='us-central1', external=False):
    scheme = 'EXTERNAL' if external else 'INTERNAL'
    resources.append({
        'google_compute_forwarding_rule': [{
            'db': [
                {
                    'name': name,
                    'target': r'${google_compute_target_pool.db.id}',
                    'port_range': '3306',
                    'region': region,
                    'load_balancing_scheme': scheme,
                    'network_tier': 'STANDARD'
                }
            ]
        }
        ]
    })