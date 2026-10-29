
import os
import secrets
import hmac
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, jsonify, request

app = Flask(__name__)

API_USERNAME = os.environ.get("EMP_USERNAME")
API_PASSWORD = os.environ.get("EMP_PASSWORD")

if not API_USERNAME or not API_PASSWORD:
    raise RuntimeError(
        "Set EMP_USERNAME and EMP_PASSWORD first."
    )

TOKEN_LIFETIME_SECONDS = 120

# Demo in-memory stores.
# Store only a hash of each random token, not the raw token.
active_tokens = {}

employees = [
    {"id": 1, "name": "Ravi", "department": "IT"},
    {"id": 2, "name": "Priya", "department": "HR"},
    {"id": 3, "name": "Arjun", "department": "Finance"},
]


def hash_token(token):
    return hmac.digest(
        b"opaque-token-demo",
        token.encode("utf-8"),
        "sha256",
    ).hex()


def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "error": "Missing or invalid Bearer token"
            }), 401

        token = parts[1]
        token_hash = hash_token(token)
        record = active_tokens.get(token_hash)

        if record is None:
            return jsonify({"error": "Invalid or revoked token"}), 401

        now = datetime.now(timezone.utc)

        if now >= record["expires_at"]:
            active_tokens.pop(token_hash, None)
            return jsonify({"error": "Token has expired"}), 401

        request.current_user = record["username"]
        return func(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Opaque-token Employee API is running"
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

    token = secrets.token_urlsafe(32)
    token_hash = hash_token(token)

    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=TOKEN_LIFETIME_SECONDS
    )

    active_tokens[token_hash] = {
        "username": username,
        "expires_at": expires_at,
    }

    return jsonify({
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": TOKEN_LIFETIME_SECONDS,
    }), 200


@app.route("/employees", methods=["GET"])
@require_token
def get_employees():
    return jsonify({
        "requested_by": request.current_user,
        "employees": employees,
    }), 200


@app.route("/employees/<int:employee_id>", methods=["GET"])
@require_token
def get_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return jsonify(employee), 200

    return jsonify({"error": "Employee not found"}), 404


@app.route("/logout", methods=["POST"])
@require_token
def logout():
    token = request.headers["Authorization"].split()[1]
    active_tokens.pop(hash_token(token), None)

    return jsonify({"message": "Token revoked successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

