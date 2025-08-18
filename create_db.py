import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect to PostgreSQL server
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='1234',
        port='5432'
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Create cursor
    cursor = connection.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE briefly;")
    print("✅ Database 'briefly' created successfully!")
    
    # Close connection
    cursor.close()
    connection.close()
    
except psycopg2.Error as e:
    if "already exists" in str(e):
        print("✅ Database 'briefly' already exists!")
    else:
        print(f"❌ Error creating database: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
