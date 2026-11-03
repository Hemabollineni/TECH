# Opaque Bearer Token Authentication

## Project Overview

This project demonstrates opaque bearer token authentication using Python, Flask, and Requests.

The Flask REST API runs on VM1, and the Python client runs on VM2.

## Features

- Username and password authentication
- Random opaque access-token generation
- Protected API endpoints using bearer tokens
- Token expiration after 120 seconds
- Employee list and individual employee retrieval
- Token revocation during logout
- Rejection of missing, invalid, expired, and revoked tokens

## Technologies Used

- Python
- Flask
- Requests
- REST API
- Opaque bearer tokens

## Project Structure

```text
opaque_employee_api/
├── employee_server.py
├── employee_client.py
├── requirements.txt
└── README.md
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/login` | Authenticate and obtain a token |
| GET | `/employees` | Retrieve all employees |
| GET | `/employees/<employee_id>` | Retrieve one employee |
| POST | `/logout` | Revoke the current token |

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the credentials on VM1 using environment variables:

```bash
export EMPLOYEE_API_USERNAME='admin'
export EMPLOYEE_API_PASSWORD='replace-with-a-strong-password'
```

Start the server on VM1:

```bash
python employee_server.py
```

Configure the API URL on VM2:

```bash
export EMPLOYEE_API_URL='http://172.20.0.10:5000'
```

Run the client on VM2:

```bash
python employee_client.py
```

## Authentication Flow

1. The client sends login credentials to the server.
2. The server verifies the credentials and generates a random opaque token.
3. The client sends the token in the `Authorization: Bearer <token>` header.
4. The server checks the token against its active-token records.
5. Expired or revoked tokens are rejected.
6. Logout revokes the token.

## Expected Results

- Successful login and protected requests: HTTP 200
- Missing, invalid, expired, or revoked token: HTTP 401
- Successful logout: HTTP 200

## Important Notes

- Never commit passwords, access tokens, or other secrets.
- Active tokens are stored in server memory in this learning project. Restarting the server clears active-token records.
- Production applications should use HTTPS and appropriately secured token storage.

