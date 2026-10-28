
import os
import hmac
from functools import wraps

from flask import Flask, request, jsonify

from parking_db import (
    vehicle_entry,
    get_vehicle,
    vehicle_exit
)

app = Flask(__name__)


def require_authentication(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):

        expected_username = os.environ.get("PARKING_API_USERNAME")
        expected_password = os.environ.get("PARKING_API_PASSWORD")

        # Fail closed if credentials are not configured
        if not expected_username or not expected_password:
            return jsonify({
                "success": False,
                "message": "Server authentication is not configured"
            }), 500

        credentials = request.authorization

        if not credentials:
            return unauthorized_response()

        username_valid = hmac.compare_digest(
            credentials.username or "",
            expected_username
        )

        password_valid = hmac.compare_digest(
            credentials.password or "",
            expected_password
        )

        if not (username_valid and password_valid):
            return unauthorized_response()

        return route_function(*args, **kwargs)

    return wrapper


def unauthorized_response():
    response = jsonify({
        "success": False,
        "message": "Invalid or missing username/password"
    })
    response.status_code = 401
    response.headers["WWW-Authenticate"] = 'Basic realm="Parking API"'
    return response


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Parking Lot REST API is running"
    })


@app.route("/entry", methods=["POST"])
@require_authentication
def entry():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "A valid JSON object is required"
        }), 400

    required_fields = [
        "vehicle_number",
        "vehicle_type",
        "owner_name",
        "age",
        "email",
        "mobile"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "message": f"{field} is required"
            }), 400

    result = vehicle_entry(
        data["vehicle_number"],
        data["vehicle_type"],
        data["owner_name"],
        data["age"],
        data["email"],
        data["mobile"]
    )

    if result["success"]:
        return jsonify(result), 201

    return jsonify(result), 400


@app.route("/vehicle/<vehicle_number>", methods=["GET"])
@require_authentication
def get_vehicle_details(vehicle_number):

    vehicle = get_vehicle(vehicle_number)

    if not vehicle:
        return jsonify({
            "success": False,
            "message": "Vehicle not found in parking lot"
        }), 404

    return jsonify({
        "success": True,
        "vehicle": vehicle
    })


@app.route("/exit", methods=["POST"])
@require_authentication
def exit_vehicle():

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "vehicle_number" not in data:
        return jsonify({
            "success": False,
            "message": "vehicle_number is required"
        }), 400

    result = vehicle_exit(data["vehicle_number"])

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 400


if __name__ == "__main__":

    if not os.environ.get("PARKING_API_USERNAME") or not os.environ.get(
        "PARKING_API_PASSWORD"
    ):
        raise RuntimeError(
            "Set PARKING_API_USERNAME and PARKING_API_PASSWORD first"
        )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
