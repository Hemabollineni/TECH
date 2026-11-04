# SSH Database Singleton Project

## Project Description
This project connects to a PostgreSQL database on a remote Ubuntu VM through an SSH tunnel.

It uses the Singleton design pattern to ensure only one SSHDatabase object is created.

## Technologies Used
- Python
- PostgreSQL
- SSH Tunnel
- Psycopg2
- SSHTunnel

## Project Structure
- ssh_database.py - Singleton class, SSH connection, database connection and CRUD operations.
- requirements.txt - Required Python packages.

## Features
1. Singleton object creation
2. SSH tunnel connection
3. PostgreSQL database connection
4. Add employee records
5. Fetch employee records
6. Update employee records
7. Delete employee records

## Setup
Install dependencies:

pip install -r requirements.txt

## Run
python3 ssh_database.py

Enter the VM2 SSH password and PostgreSQL password when prompted.

## Configuration
The current example connects to:
- Remote VM: 172.20.0.11
- SSH username: root
- Database: school_db
- Database user: singleton_user
- Table: employees
