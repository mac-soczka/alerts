alert_schema = {
    "type": "object",
    "properties": {
        "cryptocurrency": {"type": "string"},
        "exchange_currency": {"type": "string"},
        "base_value": {"type": "number"},
        "trigger_value": {"type": "number"},
        "trigger_type": {"type": "string"},
        "user_id": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
        "expires_at": {"type": "string", "format": "date-time"},
        "active": {"type": "boolean"}
    },
    "required": ["cryptocurrency", "base_value", "trigger_value", "trigger_type", "user_id", "expires_at"]
}