prices_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "cryptocurrency": {"type": "string", "maxLength": 20},
        "timestamp": {"type": "string", "format": "date-time"},
        "value": {"type": "number"},
    },
    "required": ["cryptocurrency", "value"],
    "additionalProperties": False,
}