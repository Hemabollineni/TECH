
# Public-Key Authentication REST API

## Overview
A REST API project demonstrating public-key authentication using Python Flask, Ed25519 digital signatures, and HTTP requests.

## Technologies
- Python
- Flask
- Requests
- Cryptography
- Ed25519

## Project Structure

public_key_rest_api/
├── server.py
├── client.py
├── generate_keys.py
├── requirements.txt
└── README.md

## Authentication Workflow

1. Generate an Ed25519 private/public key pair on VM2.
2. Keep the private key securely on the client.
3. Transfer the public key to VM1.
4. Client signs HTTP requests using its private key.
5. Server verifies signatures using the public key.
6. Server checks timestamps and nonces to prevent replay attacks.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Check server status |
| GET | /products | Retrieve authenticated product data |

## Security Tests

1. Valid signature - HTTP 200
2. Missing authentication headers - HTTP 401
3. Tampered signature - HTTP 401
4. Replayed request - HTTP 401

## Run the Project

Install dependencies:

pip install -r requirements.txt

Start the server on VM1:

python server.py

Run the client on VM2:

python client.py

## Important

Never upload private keys to GitHub.
Use HTTPS and persistent replay protection in production.

