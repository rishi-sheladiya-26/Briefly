from django.core.management.base import BaseCommand
from news.scraper import scrape_news_articles

class Command(BaseCommand):
    help = 'Scrape news articles and save to database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting news scraping...'))
        
        try:
            scrape_news_articles()
            self.stdout.write(
                self.style.SUCCESS('Successfully scraped and saved articles to database!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during scraping: {e}')
            )
