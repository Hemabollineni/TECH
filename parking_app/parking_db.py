import psycopg2
from datetime import datetime
import math

def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="parkinglot",
        user="postgres",
        password="root123"
    )

    return connection


def find_available_slot(vehicle_type):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT slot_number
        FROM parkingslots
        WHERE vehicle_type = %s
        AND status = 'available'
        ORDER BY slot_id
        LIMIT 1;
    """

    cursor.execute(query, (vehicle_type,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return result[0]

    return None

def vehicle_entry(
    vehicle_number,
    vehicle_type,
    owner_name,
    age,
    email,
    mobile
):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        # Check whether vehicle is already inside
        cursor.execute(
            """
            SELECT vehicle_number
            FROM entrydetails
            WHERE vehicle_number = %s
            AND active = TRUE;
            """,
            (vehicle_number,)
        )

        existing_vehicle = cursor.fetchone()

        if existing_vehicle:
            return {
                "success": False,
                "message": "Vehicle is already inside the parking lot."
            }

        # Find available slot
        cursor.execute(
            """
            SELECT slot_number
            FROM parkingslots
            WHERE vehicle_type = %s
            AND status = 'available'
            ORDER BY slot_id
            LIMIT 1;
            """,
            (vehicle_type,)
        )

        slot = cursor.fetchone()

        if not slot:
            return {
                "success": False,
                "message": "No parking slot available for this vehicle type."
            }

        slot_number = slot[0]

        # Mark slot as occupied
        cursor.execute(
            """
            UPDATE parkingslots
            SET status = 'occupied'
            WHERE slot_number = %s;
            """,
            (slot_number,)
        )

        # Insert entry details
        cursor.execute(
            """
            INSERT INTO entrydetails
            (
                vehicle_number,
                vehicle_type,
                owner_name,
                age,
                email,
                mobile,
                slot_number,
                entry_time,
                active
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s,
                CURRENT_TIMESTAMP,
                TRUE
            )
            RETURNING entry_id, entry_time;
            """,
            (
                vehicle_number,
                vehicle_type,
                owner_name,
                age,
                email,
                mobile,
                slot_number
            )
        )

        result = cursor.fetchone()

        entry_id = result[0]
        entry_time = result[1]

        connection.commit()

        return {
            "success": True,
            "message": "Vehicle entered successfully.",
            "entry_id": entry_id,
            "vehicle_number": vehicle_number,
            "vehicle_type": vehicle_type,
            "owner_name": owner_name,
            "slot_number": slot_number,
            "entry_time": str(entry_time)
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": str(error)
        }

    finally:

        cursor.close()
        connection.close()

def get_vehicle(vehicle_number):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            entry_id,
            vehicle_number,
            vehicle_type,
            owner_name,
            age,
            email,
            mobile,
            slot_number,
            entry_time
        FROM entrydetails
        WHERE vehicle_number = %s
        AND active = TRUE;
        """,
        (vehicle_number,)
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if not result:
        return None

    return {
        "entry_id": result[0],
        "vehicle_number": result[1],
        "vehicle_type": result[2],
        "owner_name": result[3],
        "age": result[4],
        "email": result[5],
        "mobile": result[6],
        "slot_number": result[7],
        "entry_time": result[8]
    }


def calculate_bill(vehicle_type, entry_time, exit_time):

    # Calculate duration
    duration = exit_time - entry_time

    total_seconds = duration.total_seconds()

    # Convert seconds to hours
    actual_hours = total_seconds / 3600

    # Charge for every started hour
    chargeable_hours = math.ceil(actual_hours)

    # Minimum one hour
    if chargeable_hours < 1:
        chargeable_hours = 1

    # Set rate
    if vehicle_type == "2-wheeler":
        rate_per_hour = 20

    elif vehicle_type == "4-wheeler":
        rate_per_hour = 30

    else:
        return None

    total_amount = chargeable_hours * rate_per_hour

    return {
        "actual_hours": round(actual_hours, 2),
        "chargeable_hours": chargeable_hours,
        "rate_per_hour": rate_per_hour,
        "total_amount": total_amount
    }

def vehicle_exit(vehicle_number):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        # Get currently parked vehicle
        cursor.execute(
            """
            SELECT
                entry_id,
                vehicle_number,
                vehicle_type,
                slot_number,
                entry_time
            FROM entrydetails
            WHERE vehicle_number = %s
            AND active = TRUE;
            """,
            (vehicle_number,)
        )

        vehicle = cursor.fetchone()

        if not vehicle:
            return {
                "success": False,
                "message": "Vehicle not found in the parking lot."
            }

        entry_id = vehicle[0]
        vehicle_number = vehicle[1]
        vehicle_type = vehicle[2]
        slot_number = vehicle[3]
        entry_time = vehicle[4]

        # Current exit time
        exit_time = datetime.now()

        # Calculate bill
        bill = calculate_bill(
            vehicle_type,
            entry_time,
            exit_time
        )

        if not bill:
            return {
                "success": False,
                "message": "Invalid vehicle type."
            }

        # Insert exit details
        cursor.execute(
            """
            INSERT INTO exitdetails
            (
                entry_id,
                vehicle_number,
                slot_number,
                entry_time,
                exit_time,
                parking_hours,
                rate_per_hour,
                total_amount
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING exit_id;
            """,
            (
                entry_id,
                vehicle_number,
                slot_number,
                entry_time,
                exit_time,
                bill["chargeable_hours"],
                bill["rate_per_hour"],
                bill["total_amount"]
            )
        )

        exit_id = cursor.fetchone()[0]

        # Mark entry as inactive
        cursor.execute(
            """
            UPDATE entrydetails
            SET active = FALSE
            WHERE entry_id = %s;
            """,
            (entry_id,)
        )

        # Free the parking slot
        cursor.execute(
            """
            UPDATE parkingslots
            SET status = 'available'
            WHERE slot_number = %s;
            """,
            (slot_number,)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Vehicle exited successfully.",
            "exit_id": exit_id,
            "entry_id": entry_id,
            "vehicle_number": vehicle_number,
            "vehicle_type": vehicle_type,
            "slot_number": slot_number,
            "entry_time": str(entry_time),
            "exit_time": str(exit_time),
            "actual_hours": bill["actual_hours"],
            "chargeable_hours": bill["chargeable_hours"],
            "rate_per_hour": bill["rate_per_hour"],
            "total_amount": bill["total_amount"]
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "message": str(error)
        }

    finally:

        cursor.close()
        connection.close()

if __name__ == "__main__":

    print("Parking database functions loaded successfully.")
