
import getpass
import os

import requests

API_URL = os.environ.get(
    "EMPLOYEE_API_URL",
    "http://172.20.0.10:5000"
).rstrip("/")


def main():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    # Step 1: Authenticate and obtain the JWT.
    try:
        response = requests.post(
            f"{API_URL}/login",
            json={
                "username": username,
                "password": password,
            },
            timeout=5,
        )
    except requests.RequestException as error:
        print("Could not connect to the API:", error)
        return

    if response.status_code != 200:
        print("Login failed:", response.status_code, response.text)
        return

    token = response.json()["access_token"]
    print("\nLogin successful. JWT received.")
    print("Token type: Bearer")

    # Step 2: Use the token to access protected employee records.
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            f"{API_URL}/employees",
            headers=headers,
            timeout=5,
        )
    except requests.RequestException as error:
        print("Could not retrieve employees:", error)
        return

    print("\nEmployee API status:", response.status_code)
    print(response.text)

    # Step 3: Retrieve one employee using the same token.
    try:
        response = requests.get(
            f"{API_URL}/employees/1",
            headers=headers,
            timeout=5,
        )
    except requests.RequestException as error:
        print("Could not retrieve employee:", error)
        return

    print("\nSingle employee status:", response.status_code)
    print(response.text)


if __name__ == "__main__":
    main()

