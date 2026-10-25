from flask import Flask, request, jsonify

from parking_db import (
    vehicle_entry,
    get_vehicle,
    vehicle_exit
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Parking Lot REST API is running"
    })

@app.route("/entry", methods=["POST"])
def entry():

    data = request.get_json()

    # Check required data
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

    print("DEBUG vehicle_type:", repr(data["vehicle_type"]))

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
def exit_vehicle():

    data = request.get_json()

    if not data or "vehicle_number" not in data:

        return jsonify({
            "success": False,
            "message": "vehicle_number is required"
        }), 400

    vehicle_number = data["vehicle_number"]

    result = vehicle_exit(vehicle_number)

    if result["success"]:

        return jsonify(result), 200

    return jsonify(result), 400

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
