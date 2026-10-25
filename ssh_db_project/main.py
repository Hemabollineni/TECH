
import os
import getpass
import paramiko
import psycopg2


class SSHDatabase:

    def __init__(self, ip, user, age, db):
        self.ip = ip
        self.user = user
        self.age = age
        self.db = db

        self.ssh = None
        self.connection = None

    # ---------------- SSH CONNECTION ----------------

    def ssh_connect(self):
        password = getpass.getpass("Enter VM2 SSH password: ")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        self.ssh.connect(
            hostname=self.ip,
            username=self.user,
            password=password,
            timeout=10
        )

        print("SSH connected successfully")

    # ---------------- EXECUTE SSH COMMAND ----------------

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

    # ---------------- DATABASE CONNECTION ----------------

    def db_connect(self, ip, db):
        password = getpass.getpass(
            "Enter PostgreSQL password: "
        )

        self.connection = psycopg2.connect(
            host=ip,
            port=5432,
            dbname=db,
            user=os.getenv("PGUSER", "postgres"),
            password=password
        )

        print("Database connected successfully")

    # ---------------- CREATE TABLE ----------------

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INTEGER NOT NULL,
            department VARCHAR(100) NOT NULL
        );
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

        self.connection.commit()
        print("Employees table is ready")

    # ---------------- CREATE ----------------

    def create(self, name, age, department):
        query = """
        INSERT INTO employees (name, age, department)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query, (name, age, department)
                )
                employee_id = cursor.fetchone()[0]

            self.connection.commit()
            print("Employee created. ID:", employee_id)

        except Exception:
            self.connection.rollback()
            raise
        return employee_id        
    # ---------------- READ ----------------

    def read(self):
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

    # ---------------- UPDATE ----------------

    def update(self, employee_id, new_department):
        query = """
        UPDATE employees
        SET department = %s
        WHERE id = %s
        RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query, (new_department, employee_id)
                )
                updated = cursor.fetchone()

            self.connection.commit()

            if updated:
                print("Employee updated")
            else:
                print("Employee ID not found")

        except Exception:
            self.connection.rollback()
            raise

    # ---------------- DELETE ----------------

    def delete(self, employee_id):
        query = """
        DELETE FROM employees
        WHERE id = %s
        RETURNING id;
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (employee_id,))
                deleted = cursor.fetchone()

            self.connection.commit()

            if deleted:
                print("Employee deleted")
            else:
                print("Employee ID not found")

        except Exception:
            self.connection.rollback()
            raise

    # ---------------- CLOSE CONNECTIONS ----------------

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

        if self.ssh is not None:
            self.ssh.close()
            self.ssh = None

        print("Connections closed")


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":

    obj = SSHDatabase(
        ip="172.20.0.11",
        user="root",
        age=25,
        db="school_db"
    )

    try:
        # Connect to VM2 through SSH
        obj.ssh_connect()

        # Run a command on VM2
        obj.exe_get_out("hostname")
        obj.exe_get_out("whoami")

        # Connect to PostgreSQL running on VM1
        obj.db_connect("127.0.0.1", obj.db)

        # Prepare the table
        obj.create_table()

        # CREATE
        employee_id = obj.create("Hema", 23, "Python")


        # READ
        obj.read()

        # UPDATE: change employee 1's department
        # Replace 1 with the ID printed during CREATE if needed.
        obj.update(employee_id, "Data Analytics")

        # READ again to verify the update
        obj.read()

        # DELETE is intentionally not automatic.
        # Call obj.delete(employee_id) when you want to delete.

    finally:
        obj.close()
