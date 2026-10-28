
import getpass
import requests

BASE_URL = "http://172.20.0.10:5000"
AUTH = None


def print_response(response):
    print("\nStatus Code:", response.status_code)

    try:
        print("Response:")
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print("Response body:", response.text)


def vehicle_entry():

    print("\n==============================")
    print("       VEHICLE ENTRY")
    print("==============================")

    vehicle_number = input("Enter vehicle number: ")
    vehicle_type = input("Enter vehicle type (2-wheeler/4-wheeler): ")
    owner_name = input("Enter owner name: ")

    try:
        age = int(input("Enter age: "))
    except ValueError:
        print("Age must be a number.")
        return

    email = input("Enter email: ")
    mobile = input("Enter mobile number: ")

    data = {
        "vehicle_number": vehicle_number,
        "vehicle_type": vehicle_type,
        "owner_name": owner_name,
        "age": age,
        "email": email,
        "mobile": mobile
    }

    try:
        response = requests.post(
            BASE_URL + "/entry",
            json=data,
            auth=AUTH,
            timeout=10
        )
        print_response(response)

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)


def get_vehicle():

    print("\n==============================")
    print("       GET VEHICLE")
    print("==============================")

    vehicle_number = input("Enter vehicle number: ")

    try:
        response = requests.get(
            BASE_URL + "/vehicle/" + requests.utils.quote(
                vehicle_number, safe=""
            ),
            auth=AUTH,
            timeout=10
        )
        print_response(response)

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)


def vehicle_exit():

    print("\n==============================")
    print("       VEHICLE EXIT")
    print("==============================")

    vehicle_number = input("Enter vehicle number: ")

    data = {
        "vehicle_number": vehicle_number
    }

    try:
        response = requests.post(
            BASE_URL + "/exit",
            json=data,
            auth=AUTH,
            timeout=10
        )
        print_response(response)

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)


def main():

    global AUTH

    print("==============================")
    print("   PARKING API LOGIN")
    print("==============================")

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    AUTH = (username, password)

    # Check credentials before displaying the menu
    try:
        response = requests.get(
            BASE_URL + "/vehicle/__authentication_check__",
            auth=AUTH,
            timeout=10
        )

        if response.status_code == 401:
            print("Login failed: invalid username or password.")
            return

        if response.status_code != 404:
            print("Server returned unexpected status:", response.status_code)
            print_response(response)
            return

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)
        return

    print("Login successful.")

    while True:

        print("\n==============================")
        print("       PARKING CLIENT")
        print("==============================")
        print("1. Vehicle Entry")
        print("2. Get Vehicle Details")
        print("3. Vehicle Exit")
        print("4. Exit")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            vehicle_entry()

        elif choice == "2":
            get_vehicle()

        elif choice == "3":
            vehicle_exit()

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
