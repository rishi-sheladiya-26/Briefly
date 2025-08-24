#!/usr/bin/env python
"""
Test saving scraped articles to Supabase database
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsAggregator.settings')
django.setup()

from news.scraper import scrape_news_articles, save_article_to_db
from news.models import Article

def test_save_to_database():
    """Test scraping and saving articles to database"""
    print("🗄️ Testing Supabase Database Operations...")
    print("=" * 60)
    
    # Get initial count
    initial_count = Article.objects.count()
    print(f"📊 Initial articles in database: {initial_count}")
    
    # Scrape articles
    print("\n📡 Scraping fresh articles...")
    articles = scrape_news_articles()
    
    if not articles:
        print("❌ No articles to save")
        return
        
    print(f"✅ Scraped {len(articles)} articles")
    
    # Save articles to database
    saved_count = 0
    print("\n💾 Saving to Supabase database...")
    
    for i, article_data in enumerate(articles, 1):
        try:
            # Check if already exists
            if Article.objects.filter(url=article_data['url']).exists():
                print(f"  {i}. ⚠️  Already exists: {article_data['title'][:50]}...")
                continue
                
            # Save to database
            saved_article = save_article_to_db(article_data)
            print(f"  {i}. ✅ Saved (ID: {saved_article.id}): {article_data['title'][:50]}...")
            saved_count += 1
            
        except Exception as e:
            print(f"  {i}. ❌ Error saving: {e}")
    
    # Check final count
    final_count = Article.objects.count()
    new_articles = final_count - initial_count
    
    print(f"\n📈 Results:")
    print(f"  • Initial count: {initial_count}")
    print(f"  • Final count: {final_count}")
    print(f"  • New articles added: {new_articles}")
    print(f"  • Articles attempted: {len(articles)}")
    
    if new_articles > 0:
        print("✅ Database operations working perfectly!")
        
        # Show latest articles
        print("\n📰 Latest articles in database:")
        latest_articles = Article.objects.all()[:5]
        for article in latest_articles:
            print(f"  • {article.title[:60]}... (ID: {article.id})")
    else:
        print("ℹ️ No new articles added (likely duplicates)")
    
    print("\n" + "=" * 60)
    print("✨ Database test completed!")

if __name__ == "__main__":
    test_save_to_database()
