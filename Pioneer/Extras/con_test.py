import mysql.connector
from mysql.connector import Error

def create_connection_pool():
    dbconfig = {
        "host": "localhost",
        "user": "root",
        "password": "SIESCE@02",
        "database": "plot_details_db",
        "pool_name": "erp_pool",
        "pool_size": 10,
        "connection_timeout": 10  # 10 seconds timeout for establishing connection
    }
    return mysql.connector.pooling.MySQLConnectionPool(**dbconfig)

def test_connection_pool():
    connection = None
    cursor = None
    try:
        pool = create_connection_pool()
        print("Connection pool created successfully.")

        connection = pool.get_connection()
        print("Successfully retrieved a connection from the pool.")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"Connected to database: {db_name[0]}")

        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    test_connection_pool()
