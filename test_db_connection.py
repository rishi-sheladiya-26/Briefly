#!/usr/bin/env python
"""
Test Supabase database connection and fix schema issues
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsAggregator.settings')
django.setup()

from django.db import connection, transaction
from django.core.management import execute_from_command_line
from news.models import Article

def test_database_connection():
    """Test the database connection and schema"""
    print("🔗 Testing Supabase Database Connection...")
    print("=" * 60)
    
    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version[:50]}...")
            
            # Check if news_article table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'news_article'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            if table_exists:
                print("✅ news_article table exists")
                
                # Check table structure
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'news_article' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                
                print("\n📋 Current table structure:")
                for col_name, data_type, nullable in columns:
                    print(f"  • {col_name}: {data_type} {'(nullable)' if nullable == 'YES' else '(not null)'}")
                
                # Check if problematic columns exist
                problem_columns = []
                for col_name, _, nullable in columns:
                    if col_name in ['is_processed', 'status'] and nullable == 'NO':
                        problem_columns.append(col_name)
                
                if problem_columns:
                    print(f"\n⚠️  Found problematic columns: {problem_columns}")
                    print("🔧 Fixing database schema...")
                    
                    # Make problematic columns nullable or drop them
                    for col in problem_columns:
                        try:
                            cursor.execute(f"ALTER TABLE news_article ALTER COLUMN {col} DROP NOT NULL;")
                            print(f"✅ Made {col} nullable")
                        except Exception as e:
                            try:
                                cursor.execute(f"ALTER TABLE news_article DROP COLUMN {col};")
                                print(f"✅ Dropped {col} column")
                            except Exception as e2:
                                print(f"❌ Could not fix {col}: {e2}")
                
            else:
                print("⚠️  news_article table doesn't exist, running migrations...")
                
        # Test Article model operations
        print("\n🧪 Testing Article model operations...")
        
        # Count existing articles
        article_count = Article.objects.count()
        print(f"📊 Current articles in database: {article_count}")
        
        # Test creating a sample article
        try:
            from django.utils import timezone
            
            test_article, created = Article.objects.get_or_create(
                url="https://test.example.com/test-article",
                defaults={
                    'title': 'Test Article',
                    'category': 'Test',
                    'full_text': 'This is a test article to verify database connectivity.',
                    'summary': 'Test summary.',
                    'publication_date': timezone.now(),
                }
            )
            
            if created:
                print("✅ Successfully created test article")
                # Clean up test article
                test_article.delete()
                print("✅ Cleaned up test article")
            else:
                print("✅ Test article already exists (connection working)")
                
        except Exception as e:
            print(f"❌ Error testing Article operations: {e}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check if your Supabase password is correct in .env file")
        print("2. Ensure your Supabase project is active")
        print("3. Verify network connectivity")
        return False
        
    print("\n" + "=" * 60)
    print("✅ Database connection test completed!")
    return True

def run_migrations():
    """Run Django migrations"""
    print("\n🔄 Running Django migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    if test_database_connection():
        run_migrations()
