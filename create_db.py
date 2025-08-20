import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    # Test connection to cloud PostgreSQL database
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        sslmode='require'  # Required for cloud databases
    )
    
    # Create cursor and test the connection
    cursor = connection.cursor()
    
    # Test query to verify connection
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("✅ Successfully connected to cloud PostgreSQL database!")
    print(f"📊 Database version: {db_version[0]}")
    
    # Check if we can create tables (permissions test)
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public'
        );
    """)
    print("✅ Database permissions verified!")
    print("🎉 Your cloud database is ready for Django migrations!")
    
    # Close connection
    cursor.close()
    connection.close()
    
except psycopg2.Error as e:
    print(f"❌ Database connection error: {e}")
    print("\n🔧 Please check your .env file and ensure:")
    print("   1. DB_HOST is correct (should end with .supabase.co)")
    print("   2. DB_USER is correct (usually 'postgres')")
    print("   3. DB_PASSWORD matches your Supabase password")
    print("   4. DB_PORT is 5432")
    print("   5. DB_NAME is 'postgres'")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
