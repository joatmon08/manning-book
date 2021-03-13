class NetworkSingleton:
    def __init__(self):
        self.data = self._build()

    def _build(self):
        data = []
        data.append({
            'aws_region': [{
                'current': [{}]
            }]
        })
        data.append({
            'aws_vpc': [{
                'default': [{
                    'default': True
                }]
            }]
        })
        return data
