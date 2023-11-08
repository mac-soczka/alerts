from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Numeric, Boolean
from datetime import datetime

db = SQLAlchemy()

time_format = '%Y-%m-%dT%H:%M'


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cryptocurrency = db.Column(db.String(10), nullable=False)
    exchange_currency = db.Column(db.String(10), nullable=False)
    base_value = db.Column(Numeric(precision=10, scale=2), nullable=False)
    trigger_value = db.Column(db.Float, nullable=False)
    trigger_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(DateTime, nullable=False)
    expires_at = db.Column(DateTime, nullable=False)
    active = db.Column(Boolean, default=True)

    def __init__(self, cryptocurrency, exchange_currency, base_value, trigger_value, trigger_type, user_id, created_at, expires_at, active=True):
        self.cryptocurrency = cryptocurrency
        self.exchange_currency = exchange_currency
        self.base_value = round(float(base_value), 2)
        self.trigger_value = trigger_value
        self.trigger_type = trigger_type
        self.user_id = user_id
        self.created_at = created_at
        self.expires_at = datetime.strptime(expires_at, time_format)
        self.active = active

    def to_dict(self):
        return {
            'id': self.id,
            'cryptocurrency': self.cryptocurrency,
            'exchange_currency': self.exchange_currency,
            'base_value': self.base_value,
            'trigger_value': self.trigger_value,
            'trigger_type': self.trigger_type,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'active': self.active,
        }


class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cryptocurrency = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(DateTime, nullable=False)
    value = db.Column(Numeric(precision=10, scale=2), nullable=False)
