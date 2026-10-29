
import os
import hmac
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Flask, jsonify, request

app = Flask(__name__)

# Read credentials and signing key from environment variables.
API_USERNAME = os.environ.get("EMP_USERNAME")
API_PASSWORD = os.environ.get("EMP_PASSWORD")
JWT_SECRET = os.environ.get("EMP_JWT_SECRET")

if not API_USERNAME or not API_PASSWORD or not JWT_SECRET:
    raise RuntimeError(
        "Set EMP_USERNAME, EMP_PASSWORD, "
        "and EMP_JWT_SECRET before starting the server."
    )

JWT_ALGORITHM = "HS256"
TOKEN_LIFETIME_MINUTES = 2

# Demo data: stored in memory, not in a database.
employees = [
    {"id": 1, "name": "Ravi", "department": "IT"},
    {"id": 2, "name": "Priya", "department": "HR"},
    {"id": 3, "name": "Arjun", "department": "Finance"},
]


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "error": "Missing or invalid Bearer token"
            }), 401

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
                options={"require": ["exp", "iat", "sub"]},
            )

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        request.current_user = payload["sub"]
        return func(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Employee Management API is running"
    }), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body required"}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({
            "error": "Username and password are required"
        }), 400

    username_ok = hmac.compare_digest(username, API_USERNAME)
    password_ok = hmac.compare_digest(password, API_PASSWORD)

    if not (username_ok and password_ok):
        return jsonify({"error": "Invalid credentials"}), 401

    now = datetime.now(timezone.utc)

    payload = {
        "sub": username,
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_LIFETIME_MINUTES),
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return jsonify({
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": TOKEN_LIFETIME_MINUTES * 60,
    }), 200


@app.route("/employees", methods=["GET"])
@token_required
def get_employees():
    return jsonify({
        "requested_by": request.current_user,
        "employees": employees,
    }), 200


@app.route("/employees/<int:employee_id>", methods=["GET"])
@token_required
def get_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return jsonify(employee), 200

    return jsonify({"error": "Employee not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

