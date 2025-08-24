#!/usr/bin/env python
"""
Simple test script for the news scraper
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsAggregator.settings')
django.setup()

from news.scraper import scrape_news_articles, save_article_to_db

def test_scraping():
    """Test the news scraping functionality"""
    print("🚀 Testing News Scraper...")
    print("=" * 50)
    
    # Test scraping
    try:
        articles = scrape_news_articles()
        
        if articles:
            print(f"✅ Success! Found {len(articles)} articles")
            
            for i, article_data in enumerate(articles, 1):
                print(f"\nArticle {i}:")
                print(f"  📰 Title: {article_data['title'][:60]}...")
                print(f"  🔗 URL: {article_data['url']}")
                print(f"  📂 Category: {article_data['category']}")
                print(f"  📝 Text length: {len(article_data['full_text'])} characters")
                
                # Test saving to database
                try:
                    saved_article = save_article_to_db(article_data)
                    print(f"  💾 Saved to database with ID: {saved_article.id}")
                except Exception as e:
                    print(f"  ❌ Error saving to database: {e}")
        else:
            print("❌ No articles found")
            
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("✨ Test completed!")

if __name__ == "__main__":
    test_scraping()
