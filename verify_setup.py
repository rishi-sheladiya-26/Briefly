#!/usr/bin/env python
"""
Quick setup verification script for friends
"""
import os
import django
from pathlib import Path
import sys

# Setup Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsAggregator.settings')
django.setup()

from django.conf import settings
from django.db import connection
from news.models import Article

def main():
    print("🔍 NEWSAGGREGATOR SETUP VERIFICATION")
    print("=" * 50)
    
    # Check .env file
    print("\n1. 📁 Checking .env file...")
    if os.path.exists('.env'):
        print("   ✅ .env file found")
        
        with open('.env', 'r') as f:
            env_content = f.read()
        
        if 'USE_CLOUD_DB=True' in env_content:
            print("   ✅ USE_CLOUD_DB is set to True")
        elif 'USE_CLOUD_DB=False' in env_content:
            print("   ❌ USE_CLOUD_DB is set to False")
            print("   🔧 FIX: Change USE_CLOUD_DB=False to USE_CLOUD_DB=True in .env file")
            return False
        else:
            print("   ⚠️  USE_CLOUD_DB not found in .env file")
    else:
        print("   ❌ .env file not found!")
        return False
    
    # Check database connection
    print("\n2. 🗄️  Checking database connection...")
    db_config = settings.DATABASES['default']
    
    if 'postgresql' in db_config['ENGINE']:
        print("   ✅ Using PostgreSQL (Supabase)")
        print(f"   🌐 Host: {db_config.get('HOST', 'Not specified')}")
    else:
        print("   ❌ Using SQLite (local database)")
        print("   🔧 FIX: Check .env file and ensure USE_CLOUD_DB=True")
        return False
    
    # Test database connectivity
    print("\n3. 🔗 Testing database connectivity...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            if version and 'PostgreSQL' in version[0]:
                print("   ✅ Connected to PostgreSQL database")
            else:
                print("   ❌ Not connected to PostgreSQL")
                return False
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        return False
    
    # Check articles
    print("\n4. 📰 Checking articles in database...")
    try:
        article_count = Article.objects.count()
        print(f"   📊 Found {article_count} articles in database")
        
        if article_count > 0:
            latest = Article.objects.first()
            print(f"   📝 Latest: {latest.title[:40]}...")
            print(f"   🕒 Added: {latest.created_at.strftime('%Y-%m-%d %H:%M')}")
        else:
            print("   ℹ️  No articles yet - try scraping some news!")
    except Exception as e:
        print(f"   ❌ Error accessing articles: {e}")
        return False
    
    # Final result
    print("\n" + "=" * 50)
    print("🎉 SETUP VERIFICATION COMPLETE!")
    print("✅ Your NewsAggregator is properly connected to the shared database!")
    print("✅ You and your friend will see the same news articles!")
    print("\n🚀 To start the server, run: python manage.py runserver 8000")
    print("🌐 Then visit: http://127.0.0.1:8000")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup verification failed!")
        print("📖 Please check FRIEND_SETUP_GUIDE.md for troubleshooting steps.")
        sys.exit(1)
