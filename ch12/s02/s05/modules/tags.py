import datetime

EXPIRATION_DATE_FORMAT = '%Y-%m-%d'


class DefaultTags():
    def __init__(self, environment, long_term=False):
        self.tags = {
            'customer': 'community',
            'automated': True,
            'cost_center': 123456,
            'environment': environment
        }
        if environment != 'prod' and not long_term:
            self._set_expiration()
    
    def get(self):
        return self.tags

    def _set_expiration(self):
        expiration_date = (
            datetime.datetime.now() +
            datetime.timedelta(days=7)
        ).strftime(EXPIRATION_DATE_FORMAT)
        self.tags['expiration'] = expiration_date
