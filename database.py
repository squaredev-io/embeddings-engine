import psycopg2


def create_connection(db_url: str):
    connection = None
    try:
        connection = psycopg2.connect(db_url)
        print("Connection to PostgreSQL DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")


create_database_query = """
CREATE DATABASE IF NOT EXISTS squares;
"""
