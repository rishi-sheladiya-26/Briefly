#!/usr/bin/env python
"""
Script to check which database is currently being used
"""
import os
import django
from pathlib import Path

# Add the project directory to the path
import sys
sys.path.append(str(Path(__file__).parent))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsAggregator.settings')
django.setup()

from django.conf import settings
from django.db import connection
from news.models import Article

def main():
    print("=== DATABASE CONNECTION CHECKER ===")
    print()
    
    # Get database configuration
    db_config = settings.DATABASES['default']
    
    print(f"🔧 Database Engine: {db_config['ENGINE']}")
    
    if 'sqlite' in db_config['ENGINE']:
        print(f"📁 Database File: {db_config['NAME']}")
        print("⚠️  Using LOCAL SQLite database")
    else:
        print(f"🌐 Database Host: {db_config.get('HOST', 'Not specified')}")
        print(f"👤 Database User: {db_config.get('USER', 'Not specified')}")
        print(f"🗄️  Database Name: {db_config.get('NAME', 'Not specified')}")
        print("✅ Using CLOUD database (Supabase)")
    
    print()
    
    # Test database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            if version:
                print(f"📊 Database Version: {version[0]}")
            else:
                print("📊 Database Version: SQLite (local)")
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return
    
    # Count articles in database
    try:
        article_count = Article.objects.count()
        print(f"📰 Total articles in database: {article_count}")
        
        if article_count > 0:
            latest_article = Article.objects.first()
            print(f"📝 Latest article: {latest_article.title[:50]}...")
            print(f"🕒 Created at: {latest_article.created_at}")
    except Exception as e:
        print(f"❌ Error counting articles: {e}")
    
    print()
    print("=== SUMMARY ===")
    if 'sqlite' in db_config['ENGINE']:
        print("❌ Your friend is using LOCAL database - they won't see your news!")
        print("🔧 Solution: Make sure .env file has USE_CLOUD_DB=True")
    else:
        print("✅ Using SHARED database - both should see same news!")

if __name__ == "__main__":
    main()
