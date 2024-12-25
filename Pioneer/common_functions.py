import mysql.connector
from mysql.connector import Error

def extract_rows_from_db(plotdetails_uid):
    """
    Extract rows from the database based on the provided plotdetails_uid.

    Args:
        plotdetails_uid (str): The ID of the form to filter the rows.

    Returns:
        list: A list of dictionaries representing the rows from the database.
    """
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',          # Replace with your host (e.g., 'localhost' or an IP address)
            user='root',          # Replace with your MySQL username
            password='Akhatri@2023',  # Replace with your MySQL password
            database='plot_details_db'   # Replace with your database name
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Use dictionary=True for row results as dictionaries
            
            # Define the SQL query to fetch data for the given form_id
        query = "SELECT * FROM plot_details_db WHERE form_id = %s"

        # Execute the query with the provided form_id
        print(f"Executing query: {query} with form_id = {plotdetails_uid}")
        cursor.execute(query, (plotdetails_uid,))

        # Fetch all rows and convert them into a list of dictionaries
        rows = cursor.fetchall()

        return rows

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return []

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
