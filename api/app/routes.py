from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from sqlalchemy import DateTime
from datetime import datetime
from app.models import db, Alert, Prices
from app.schema.alert_schema import alert_schema
from app.schema.prices_schema import prices_schema
from jsonschema import validate, ValidationError
import dateparser

time_format = '%Y-%m-%dT%H:%M'

main_bp = Blueprint('main', __name__)

@main_bp.route('/alerts/<int:alert_id>')
def get_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({"error": "index does not exist"})

    alert_data = {
        "id": alert.id,
        "created_at": alert.created_at,
        "expires_at": alert.expires_at,
        "cryptocurrency": alert.cryptocurrency,
        "trigger_value": alert.trigger_value,
        "exchange_currency": alert.exchange_currency,
        "trigger_type": alert.trigger_type
    }

    return alert_data


@main_bp.route('/alerts', methods=['GET'])
def get_alerts():
    try:
        user_id = request.args.get('userId', None)
        print(f"UserId: {user_id}")
        if user_id is None:
            alerts = Alert.query.all()
        else:
            alerts = Alert.query.filter_by(user_id=user_id).all()

        return jsonify([{"id": alert.id,
                         "active": alert.active,
                         "created_at": alert.created_at,
                         "expires_at": alert.expires_at,
                         "cryptocurrency": alert.cryptocurrency,
                         "trigger_value": alert.trigger_value,
                         "base_value": alert.base_value,
                         "user_id" : alert.user_id,
                         "exchange_currency": alert.exchange_currency,
                         "trigger_type": alert.trigger_type} for alert in alerts])
    except Exception as e:
        print(e)


@main_bp.route('/alerts', methods=['POST'])
def create_alert():
    data = request.get_json()
    print(data)
    try:
        validate(data, alert_schema) 
        data['created_at'] = datetime.now()
        data['exchange_currency'] = "USD"
        new_alert = Alert(**data)
        db.session.add(new_alert)
        db.session.commit()
        print(new_alert.to_dict())
        return jsonify(new_alert.to_dict()), 201
    except ValidationError as e:
        print(e)
        return jsonify({"Validation error" : str(e.message)}), 400
    except Exception as e:
        print(e)
        return jsonify({"Error" : str(e)}), 500
    return jsonify({"message": "Alert created successfully"})


@main_bp.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    #input_format = '%a, %d %b %Y %H:%M:%S %Z'
    input_format = '%Y-%m-%dT%H:%M'
    try:
        alert = Alert.query.get(alert_id)
        if not alert:
            return jsonify({"error": "index does not exist"}), 500

        data = request.get_json()
        validate(data, alert_schema) 
        alert.active = data.get('active', alert.active)
        alert.cryptocurrency = data.get('cryptocurrency', alert.cryptocurrency)
        alert.trigger_value = data.get('trigger_value', alert.trigger_value)
        alert.trigger_type = data.get('trigger_type', alert.trigger_type)
        alert.base_value = data.get('base_value', alert.base_value)
        alert.exchange_currency = data.get(
            'exchange_currency', alert.exchange_currency)
        alert.expires_at = datetime.strptime(data.get("expires_at"), input_format)
        db.session.commit()
    except ValidationError as e:
        print(e)
        return jsonify({"Validation error" : str(e.message)}), 400
    except Exception as e:
        print(e)
        return jsonify({"Error" : str(e)}), 500
    return jsonify({"message": "Alert updated successfully"})


@main_bp.route('/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({"error": "index does not exist"}), 500
    try:
        db.session.delete(alert)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"error": "index does not exist"}), 500
    finally:
        return jsonify({"message": "Alert deleted successfully"})

@main_bp.route('/prices', methods=['POST'])
def add_prices():
    data = request.get_json()
    try:
        validate(data, prices_schema)
        now = datetime.now()
        data["timestamp"] = now
        new_prices = Prices(**data)
        db.session.add(new_prices)
        db.session.commit()

        return jsonify({"message": "Prices created successfully"})
    except ValidationError as e:
        return jsonify({"Validation error": str(e.message)}), 400
    except Exception as e:
        print(e)
        return jsonify({"Error": str(e)}), 500

@main_bp.route("/prices", methods=["GET"])
def get_prices():
    try:
        prices = Prices.query.order_by(Prices.timestamp.desc()).limit(3).all()

        prices_data = [{
            "id": price.id,
            "cryptocurrency": price.cryptocurrency,
            "value": price.value,
            "timestamp": price.timestamp
        } for price in prices]

        return jsonify(prices_data)
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to fetch prices"}), 500

def get_expiry_date(verbal_time_expression):
    parsed_expiry_date = dateparser.parse("in" + verbal_time_expression)
    return parsed_expiry_date
