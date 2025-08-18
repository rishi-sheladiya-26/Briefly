from django.core.management.base import BaseCommand
from news.scraper import scrape_article_content, scrape_india_today
from news.models import Article


class Command(BaseCommand):
    help = 'Test scraping functionality'

    def handle(self, *args, **options):
        self.stdout.write("Testing article scraping...")
        
        # Test individual article scraping
        test_url = "https://www.indiatoday.in/world/us-news/story/vivek-ramaswamy-hosts-cincinnati-townhall-public-safety-crime-cincinnati-beating-sarah-heringer-justice-system-holly-2766493-2025-08-05"
        
        self.stdout.write(f"Testing URL: {test_url}")
        article_data = scrape_article_content(test_url)
        
        if article_data:
            self.stdout.write(self.style.SUCCESS(f"✓ Successfully scraped article"))
            self.stdout.write(f"Title: {article_data['title']}")
            self.stdout.write(f"Text length: {len(article_data['full_text'])}")
            self.stdout.write(f"Category: {article_data.get('category', 'N/A')}")
            
            # Test saving to database
            from news.scraper import save_article_to_db
            try:
                saved_article = save_article_to_db(article_data)
                self.stdout.write(self.style.SUCCESS(f"✓ Successfully saved to database: {saved_article.title}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Failed to save to database: {e}"))
        else:
            self.stdout.write(self.style.ERROR("✗ Failed to scrape article"))
        
        # Test full scraper
        self.stdout.write("\nTesting full India Today scraper...")
        articles = scrape_india_today()
        self.stdout.write(f"Found {len(articles) if articles else 0} articles")
        
        # Show database stats
        total_articles = Article.objects.count()
        self.stdout.write(f"\nTotal articles in database: {total_articles}")
