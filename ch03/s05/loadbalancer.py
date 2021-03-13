class LoadBalancerFactory:
    def __init__(self, name, region='us-central1', external=False):
        self.name = name
        self.region = region
        self.external = external
        self.resources = self._build()

    def _build(self): 
        scheme = 'EXTERNAL' if self.external else 'INTERNAL'
        resources = []
        resources.append({
            'google_compute_forwarding_rule': [{
                'db': [
                    {
                        'name': self.name,
                        'target': r'${google_compute_target_pool.db.id}',
                        'port_range': '3306',
                        'region': self.region,
                        'load_balancing_scheme': scheme,
                        'network_tier': 'STANDARD'
                    }
                ]
            }
            ]
        })
        return resources