

import requests
import base64
import time
import secrets

from cryptography.hazmat.primitives import serialization

SERVER_URL = "http://ubuntu-vm1:5000"

with open("client_private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

method = "GET"
path = "/products"
timestamp = str(int(time.time()))
nonce = secrets.token_urlsafe(24)

message = (
    f"{method}\n"
    f"{path}\n"
    f"{timestamp}\n"
    f"{nonce}"
).encode("utf-8")

signature = private_key.sign(message)

headers = {
    "X-Signature": base64.b64encode(signature).decode("ascii"),
    "X-Timestamp": timestamp,
    "X-Nonce": nonce,
}

# First request
response1 = requests.get(
    SERVER_URL + path,
    headers=headers,
    timeout=5
)

print("First request:", response1.status_code)
print("Response:", response1.json())

# Replay the exact same request
response2 = requests.get(
    SERVER_URL + path,
    headers=headers,
    timeout=5
)

print("Second request:", response2.status_code)
print("Response:", response2.json())
