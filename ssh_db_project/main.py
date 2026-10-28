
import os
import getpass
import paramiko
import psycopg2


class SSHDatabase:
        
    def __init__(self, hostname, user, db):
        self.hostname = hostname
        self.user = user
        self.db = db

        self.ssh = None
        self.connection = None

        try:
            self.ssh_connect()
            self.db_connect()

        except Exception:
            self.close()
        raise
    # ---------- SSH CONNECTION ----------

    def ssh_connect(self):
        password = getpass.getpass("Enter VM2 SSH password: ")

        self.ssh = paramiko.SSHClient()

        # For a lab environment. In production, verify host keys.
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        try:
            self.ssh.connect(
                hostname=self.hostname,
                username=self.user,
                password=password,
                timeout=10
            )
            print("SSH connected successfully")

        except Exception:
            self.ssh.close()
            self.ssh = None
            raise

    # ---------- EXECUTE REMOTE COMMAND ----------

    def exe_get_out(self, command):
        if self.ssh is None:
            raise RuntimeError("Connect SSH first")

        stdin, stdout, stderr = self.ssh.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()
        exit_code = stdout.channel.recv_exit_status()

        if exit_code != 0:
            print("Command error:", error)
        else:
            print(output)

        return output

    # ---------- DATABASE CONNECTION ----------

    def db_connect(self):
        password = getpass.getpass(
            "Enter VM2 PostgreSQL password: "
        )

        try:
            self.connection = psycopg2.connect(
                host=self.hostname,
                port=5432,
                dbname=self.db,
                user=os.getenv("PGUSER", "postgres"),
                password=password,
                connect_timeout=10
            )

            print("Database connected successfully")

        except Exception:
            print("Database connection failed")
            raise

    # ---------- CREATE TABLE ----------

    def create_table(self):
        if self.connection is None:
            raise RuntimeError("Connect to database first")

        query = """
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INTEGER NOT NULL,
                department VARCHAR(100) NOT NULL
            );
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)

            self.connection.commit()
            print("Employees table is ready")

        except Exception:
            self.connection.rollback()
            raise

    # ---------- CREATE ----------

    def create_employees(self, name, age, department):
        query = """
            INSERT INTO employees (name, age, department)
            VALUES (%s, %s, %s)
            RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (name, age, department))
                employee_id = cursor.fetchone()[0]

            self.connection.commit()
            print("Employee created. ID:", employee_id)
            return employee_id

        except Exception:
            self.connection.rollback()
            raise

    # ---------- READ ----------

    def read_employees(self):
        query = """
            SELECT id, name, age, department
            FROM employees
            ORDER BY id;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            print(row)

        return rows

    # ---------- UPDATE ----------

    def update_employees(self, employee_id, name=None,
               age=None, department=None):

        if self.connection is None:
            raise RuntimeError("Connect to database first")

        changes = {}

        if name is not None:
            changes["name"] = name

        if age is not None:
            changes["age"] = age

        if department is not None:
            changes["department"] = department

        if not changes:
            print("No changes provided")
            return

        set_clause = ", ".join(
            f"{column} = %s" for column in changes
        )

        values = list(changes.values())
        values.append(employee_id)

        query = f"""
            UPDATE employees
            SET {set_clause}
            WHERE id = %s
            RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, tuple(values))
                result = cursor.fetchone()

            self.connection.commit()

            if result:
                print(f"Employee {employee_id} updated")
            else:
                print(f"Employee {employee_id} not found")

        except Exception:
            self.connection.rollback()
            raise

    # ---------- DELETE ----------

    def delete(self, employee_id):
        query = """
            DELETE FROM employees
            WHERE id = %s
            RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (employee_id,))
                result = cursor.fetchone()

            self.connection.commit()

            if result:
                print("Employee deleted")
            else:
                print("Employee ID not found")

        except Exception:
            self.connection.rollback()
            raise

    # ---------- CLOSE CONNECTIONS ----------

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

        if self.ssh is not None:
            self.ssh.close()
            self.ssh = None

        print("Connections closed")


# ---------- MAIN PROGRAM ----------
obj = None

try:
    obj = SSHDatabase(
        hostname="ubuntu-vm2",
        user="root",
        db="school_db"
    )

    # SSH connection is already established by __init__()
    obj.exe_get_out("hostname")
    obj.exe_get_out("whoami")

    
    # Prepare database table
    obj.create_table()
        
    # Create a new employee
    obj.create_employees("Max", 28 ,"IT")

    # Display existing employees
    print("\n--- Employees ---")
    obj.read_employees()

    # Update an employee interactively
    employee_id = int(input("\nEnter employee ID to update: "))

    print("Leave a field blank to keep its current value.")

    name = input("New name: ").strip()
    age_input = input("New age: ").strip()
    department = input("New department: ").strip()

    obj.update_employees(
        employee_id,
        name=name or None,
        age=int(age_input) if age_input else None,
        department=department or None
    )
    
    # Verify changes
    print("\n--- Updated Employees ---")
    obj.read_employees()

except Exception as error:
    print("Error:", error)

finally:
    if obj is not None:
        obj.close()