
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

    try:
        login_response = requests.post(
            f"{API_URL}/login",
            json={"username": username, "password": password},
            timeout=5,
        )
    except requests.RequestException as error:
        print("Connection failed:", error)
        return

    if login_response.status_code != 200:
        print("Login failed:", login_response.status_code)
        print(login_response.text)
        return

    token = login_response.json()["access_token"]
    print("\nLogin successful. Opaque token received.")

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{API_URL}/employees",
        headers=headers,
        timeout=5,
    )

    print("\nEmployee list status:", response.status_code)
    print(response.text)

    response = requests.get(
        f"{API_URL}/employees/1",
        headers=headers,
        timeout=5,
    )

    print("\nSingle employee status:", response.status_code)
    print(response.text)

    response = requests.post(
        f"{API_URL}/logout",
        headers=headers,
        timeout=5,
    )

    print("\nLogout status:", response.status_code)
    print(response.text)

    # A revoked token must no longer work.
    response = requests.get(
        f"{API_URL}/employees",
        headers=headers,
        timeout=5,
    )

    print("\nAfter logout status:", response.status_code)
    print(response.text)


if __name__ == "__main__":
    main()

