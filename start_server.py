#!/usr/bin/env python
"""
Django News Aggregator - Startup Script
"""
import os
import sys
import subprocess

def main():
    """Run the Django development server"""
    print("=" * 60)
    print("🚀 DJANGO NEWS AGGREGATOR")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found!")
        print("Please run this script from the Django project directory.")
        return
    
    print("📊 Dashboard: http://localhost:8000")
    print("📰 Articles: http://localhost:8000/articles/")
    print("🔄 Scraper: http://localhost:8000/scrape/")
    print("🔧 Admin: http://localhost:8000/admin/")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        # Run Django development server
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8000'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
