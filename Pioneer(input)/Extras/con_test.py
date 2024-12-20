from sqlalchemy import create_engine

# Database connection details
DATABASE_URL = "mysql+pymysql://root:root@localhost/inventory_db"

# Test the connection
try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")
