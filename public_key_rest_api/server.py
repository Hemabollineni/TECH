
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import base64
import time
import re

app = Flask(__name__)

# Load the client's public key
with open("client_public.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read())

# Demo product inventory
products = [
    {"id": 1, "name": "Keyboard", "price": 800},
    {"id": 2, "name": "Mouse", "price": 400},
]

# Store recently used nonces in memory.
# Suitable for this single-process learning lab only.
used_nonces = {}
MAX_CLOCK_SKEW = 60


def verify_request():
    signature_text = request.headers.get("X-Signature")
    timestamp = request.headers.get("X-Timestamp")
    nonce = request.headers.get("X-Nonce")

    if not signature_text or not timestamp or not nonce:
        return False, "Missing authentication headers"

    if not re.fullmatch(r"[A-Za-z0-9_-]{16,128}", nonce):
        return False, "Invalid nonce"

    try:
        request_time = int(timestamp)
    except ValueError:
        return False, "Invalid timestamp"

    now = int(time.time())
    if abs(now - request_time) > MAX_CLOCK_SKEW:
        return False, "Request expired"

    # Include method, path, timestamp, and nonce in the signed message.
    message = (
        f"{request.method}\n"
        f"{request.path}\n"
        f"{timestamp}\n"
        f"{nonce}"
    ).encode("utf-8")

    try:
        signature = base64.b64decode(
            signature_text, validate=True
        )
        public_key.verify(signature, message)
    except (InvalidSignature, ValueError):
        return False, "Invalid signature"

    # Only consume the nonce after signature verification.
    # The lock makes this check-and-insert atomic within this process.
    from threading import Lock
    if not hasattr(verify_request, "nonce_lock"):
        verify_request.nonce_lock = Lock()

    with verify_request.nonce_lock:
        # Remove expired nonce entries.
        for old_nonce, expiry in list(used_nonces.items()):
            if expiry < now:
                del used_nonces[old_nonce]

        if nonce in used_nonces:
            return False, "Replay detected"

        used_nonces[nonce] = request_time + MAX_CLOCK_SKEW

    return True, "Authenticated"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"}), 200


@app.route("/products", methods=["GET"])
def get_products():
    valid, message = verify_request()

    if not valid:
        return jsonify({
            "error": message
        }), 401

    return jsonify({
        "message": "Public-key authentication successful",
        "products": products
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

