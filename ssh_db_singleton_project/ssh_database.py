
import psycopg2
from sshtunnel import SSHTunnelForwarder


class SSHDatabase:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            print("Creating Singleton object")
            cls._instance = super().__new__(cls)
        else:
            print("Existing Singleton object returned")

        return cls._instance

    def __init__(self):

        if not hasattr(self, "initialized"):

            self.tunnel = None
            self.connection = None

            self.initialized = True

            print("SSH Database object initialized")

    def connect(self, ssh_password, db_password):

        self.tunnel = SSHTunnelForwarder(
            ("172.20.0.11", 22),

            ssh_username="root",
            ssh_password=ssh_password,

            remote_bind_address=("127.0.0.1", 5432),
            local_bind_address=("127.0.0.1", 5433),

            allow_agent=False
        )

        self.tunnel.start()

        print("SSH tunnel established")

        self.connection = psycopg2.connect(
            host="127.0.0.1",
            port=self.tunnel.local_bind_port,
            database="school_db",
            user="singleton_user",
            password=db_password
        )

        print("PostgreSQL connection successful")

    def fetch_employees(self):

        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT id, name, age, department FROM employees"
        )

        records = cursor.fetchall()

        cursor.close()

        return records
    
    def add_employee(self, name, age, department):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO employees (name, age, department)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, age, department))

        self.connection.commit()

        cursor.close()

        print("Employee added successfully")
    
    def delete_employee(self, employee_id):
        cursor = self.connection.cursor()

        query = """
            DELETE FROM employees
            WHERE id = %s
        """

        cursor.execute(query, (employee_id,))

        self.connection.commit()

        print("Rows deleted:", cursor.rowcount)

        cursor.close()
        
    def close(self):

        if self.connection:
            self.connection.close()
            self.connection = None
            print("Database connection closed")

        if self.tunnel:
            self.tunnel.stop()
            self.tunnel = None
            print("SSH tunnel closed")
    
    def update_employee(self, employee_id, department):
        cursor = self.connection.cursor()

        query = """
            UPDATE employees
            SET department = %s
            WHERE id = %s
        """

        cursor.execute(query, (department, employee_id))

        self.connection.commit()

        print("Rows updated:", cursor.rowcount)

        cursor.close()        


if __name__ == "__main__":

    from getpass import getpass

    db1 = SSHDatabase()
    db2 = SSHDatabase()

    print("\nSame object:", db1 is db2)

    ssh_password = getpass("Enter VM2 SSH password: ")
    db_password = getpass("Enter PostgreSQL password: ")

    try:
        db1.connect(ssh_password, db_password)

        # DELETE
        db1.delete_employee(34)

        # READ
        employees = db1.fetch_employees()

        print("\nEmployee Records:")

        for employee in employees:
            print(employee)

    except Exception as error:
        print("Error:", error)

    finally:
        db1.close()
