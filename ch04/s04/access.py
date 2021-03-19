class Infrastructure:
    def __init__(self):
        self.resources = {
            'read': [    #A
                'audit-team',    #D
                'user-01',    #B
                'user-02'    #B
            ],
            'write': [    #A
                'infrastructure-team',    #D
                'user-03',    #B
                'automation-01'    #C
            ],
            'admin': [    #A
                'manager-team'    #D
            ]
        }
