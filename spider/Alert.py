from datetime import datetime

date_format = '%a, %d %b %Y %H:%M:%S GMT'

class Alert:
    def __init__(self, active, id, cryptocurrency, exchange_currency, base_value, trigger_value, trigger_type, user_id, created_at, expires_at):
        self.id = id
        self.active = active
        self.cryptocurrency = cryptocurrency
        self.exchange_currency = exchange_currency
        self.base_value = float(base_value)
        self.trigger_value = trigger_value
        self.trigger_type = trigger_type
        self.user_id = user_id
        self.created_at = datetime.strptime(created_at, date_format)
        self.expires_at = datetime.strptime(expires_at, date_format) 
