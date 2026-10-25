import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "school_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "root123")
    )


def initialize_db():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rest_items (
                    item_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT
                )
            """)
        connection.commit()
    finally:
        connection.close()


def add_item(name, description):
    connection = get_db_connection()

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO rest_items (name, description)
                VALUES (%s, %s)
                RETURNING item_id, name, description
                """,
                (name, description)
            )
            item = cursor.fetchone()

        connection.commit()
        return dict(item)
    finally:
        connection.close()


def get_all_items():
    connection = get_db_connection()

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT item_id, name, description
                FROM rest_items
                ORDER BY item_id
            """)
            items = cursor.fetchall()
            return [dict(item) for item in items]
    finally:
        connection.close()


def get_item(item_id):
    connection = get_db_connection()

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT item_id, name, description
                FROM rest_items
                WHERE item_id = %s
                """,
                (item_id,)
            )
            item = cursor.fetchone()
            return dict(item) if item else None
    finally:
        connection.close()


def update_item(item_id, name, description):
    connection = get_db_connection()

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE rest_items
                SET name = %s, description = %s
                WHERE item_id = %s
                RETURNING item_id, name, description
                """,
                (name, description, item_id)
            )
            item = cursor.fetchone()

        connection.commit()
        return dict(item) if item else None
    finally:
        connection.close()


def delete_item(item_id):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM rest_items WHERE item_id = %s",
                (item_id,)
            )
            deleted = cursor.rowcount > 0

        connection.commit()
        return deleted
    finally:
        connection.close()
