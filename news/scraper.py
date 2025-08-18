import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
from news.models import Article
from django.utils.timezone import now

def scrape_news_articles():
    """
    Scrape news articles from multiple sources and return list
    """
    all_articles = []
    
    # Add different news sources
    sources = [
        {
            'name': 'India Today',
            'url': 'https://www.indiatoday.in/latest-news',
            'scraper': scrape_india_today
        }
    ]
    
    for source in sources:
        try:
            print(f"Scraping from {source['name']}...")
            articles = source['scraper']()
            if articles:
                all_articles.extend(articles)
            time.sleep(1)  # Be respectful to the servers
        except Exception as e:
            print(f"Error scraping {source['name']}: {e}")
            continue
    
    return all_articles

def scrape_india_today():
    """
    Scrape articles from India Today and return article data
    """
    articles = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get('https://www.indiatoday.in/latest-news', headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        article_links = soup.find_all('a', href=True)
        print(f"Found {len(article_links)} total links on page")

        story_links = []
        for link in article_links:
            href = link.get('href')
            if href and ('/story/' in href or '/news/' in href):
                story_links.append(href)
        
        print(f"Found {len(story_links)} story/news links")
        
        processed_urls = set()  # Avoid duplicates
        for href in story_links[:10]:  # Check first 10 story links
            if not href.startswith('http'):
                href = 'https://www.indiatoday.in' + href
            
            # Skip if already processed
            if href in processed_urls:
                continue
            processed_urls.add(href)
            
            print(f"Attempting to scrape: {href}")
            
            # Get article content
            article_data = scrape_article_content(href)
            if article_data:
                articles.append(article_data)
                print(f"✓ Successfully scraped: {article_data['title'][:50]}...")
                time.sleep(0.5)  # Small delay between requests
                
                # Limit to 3 successful articles for testing
                if len(articles) >= 3:
                    break
            else:
                print(f"✗ Failed to scrape content from: {href}")
                    
    except Exception as e:
        print(f"Error scraping India Today: {e}")
    
    print(f"Returning {len(articles)} articles")
    return articles

def scrape_article_content(url):
    """
    Scrape individual article content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = ''
        title_selectors = ['h1', '.headline', '.title', '[data-testid="headline"]']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                break
        
        # Extract article text
        full_text = ''
        text_selectors = [
            '.story-body p', 
            '.article-body p', 
            '.content p',
            '[data-testid="text-block"] p',
            '.post-content p'
        ]
        
        for selector in text_selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                full_text = ' '.join([p.get_text().strip() for p in paragraphs])
                break
        
        # If no specific selectors work, try generic paragraph extraction
        if not full_text:
            paragraphs = soup.find_all('p')
            full_text = ' '.join([p.get_text().strip() for p in paragraphs[:10]])
        
        # Clean up text
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        
        if len(full_text) < 100 or not title:
            return None
        
        return {
            'title': title,
            'url': url,
            'full_text': full_text,
            'publication_date': datetime.now(),
            'category': 'General'
        }
    
    except Exception as e:
        print(f"Error scraping article {url}: {e}")
        return None

def save_article_to_db(article_data):
    """
    Save article to the database and summarize
    """
    # Simple fallback summarization
    summary = simple_summary(article_data['full_text'])
    
    # Create or update the article in the database
    article, created = Article.objects.update_or_create(
        url=article_data['url'],
        defaults={
            'title': article_data['title'],
            'category': article_data.get('category', 'General'),
            'full_text': article_data['full_text'],
            'summary': summary,
            'publication_date': article_data['publication_date'],
            'updated_at': now(),
        }
    )
    
    if created:
        print(f"Saved new article: {article.title}")
    else:
        print(f"Updated existing article: {article.title}")
    
    return article

def simple_summary(text, max_sentences=3):
    """
    Simple extractive summarization
    """
    if not text:
        return ""
    
    sentences = text.split('. ')
    # Take first few sentences as summary
    if len(sentences) > max_sentences:
        return '. '.join(sentences[:max_sentences]) + '.'
    return text

def test_scraper():
    """
    Test function to check if scraping works
    """
    print("Testing news scraper...")
    articles = scrape_news_articles()
    if articles:
        print(f"Found {len(articles)} articles")
        
        for i, article in enumerate(articles[:3]):
            print(f"\nArticle {i+1}:")
            print(f"Title: {article.get('title', 'No title')}")
            print(f"URL: {article['url']}")
            print(f"Text length: {len(article.get('full_text', ''))}")
            print(f"Category: {article.get('category', 'Unknown')}")
    else:
        print("No articles found")

if __name__ == "__main__":
    test_scraper()
