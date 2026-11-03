import jwt
from datetime import datetime, timedelta, timezone

# Secret key
SECRET_KEY = "my-secret-key"

# Username
username = "hema"

# Generate JWT token
payload = {
    "username": username,
    "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("Generated JWT Token:")
print(token)


# Verify JWT token
try:
    decoded_token = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
    )

    print("\nToken is valid")
    print("Username:", decoded_token["username"])

except jwt.InvalidTokenError:
    print("Invalid or expired token")