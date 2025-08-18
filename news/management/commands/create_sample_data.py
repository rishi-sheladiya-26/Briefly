from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Article
from news.utils import summarize_text

class Command(BaseCommand):
    help = 'Create sample news articles for testing'

    def handle(self, *args, **options):
        sample_articles = [
            {
                'title': 'Breaking: Major Technology Breakthrough Announced',
                'url': 'https://example.com/tech-breakthrough',
                'category': 'Technology',
                'full_text': '''
                In a groundbreaking announcement today, researchers at a leading technology institute 
                revealed a revolutionary advancement in artificial intelligence that could transform 
                the way we interact with computers. The new system, which has been in development 
                for over three years, demonstrates unprecedented capabilities in natural language 
                processing and machine learning. Scientists believe this breakthrough could lead to 
                more intuitive human-computer interfaces and significantly improve automation across 
                various industries. The research team plans to publish their findings in a peer-reviewed 
                journal next month and has already begun collaborating with major technology companies 
                to explore commercial applications.
                ''',
            },
            {
                'title': 'Climate Change Summit Reaches Historic Agreement',
                'url': 'https://example.com/climate-summit',
                'category': 'Environment',
                'full_text': '''
                World leaders gathered at the annual Climate Change Summit have reached a historic 
                agreement on reducing global carbon emissions by 50% within the next decade. The 
                comprehensive plan includes commitments from over 190 countries to transition to 
                renewable energy sources, implement carbon pricing mechanisms, and invest in green 
                technology research. Environmental activists have hailed the agreement as a crucial 
                step forward in combating climate change, though some critics argue that the targets 
                may not be ambitious enough. The agreement also includes provisions for financial 
                assistance to developing nations to help them meet their climate goals while 
                maintaining economic growth.
                ''',
            },
            {
                'title': 'Space Exploration Mission Discovers Potential Signs of Life',
                'url': 'https://example.com/space-discovery',
                'category': 'Science',
                'full_text': '''
                A robotic mission to Mars has uncovered what scientists describe as "intriguing 
                biosignatures" that could indicate the presence of microbial life on the Red Planet. 
                The discovery was made using advanced spectrographic analysis of rock samples 
                collected from a region believed to have once contained liquid water. While researchers 
                emphasize that the findings are preliminary and require further investigation, the 
                discovery has generated significant excitement in the scientific community. The 
                mission team is now planning additional experiments to confirm their initial findings 
                and hopes to return samples to Earth for more detailed analysis within the next five years.
                ''',
            },
        ]

        created_count = 0
        for article_data in sample_articles:
            # Check if article already exists
            if not Article.objects.filter(url=article_data['url']).exists():
                # Generate summary
                summary = summarize_text(article_data['full_text'])
                
                # Create article
                Article.objects.create(
                    title=article_data['title'],
                    url=article_data['url'],
                    category=article_data['category'],
                    publication_date=timezone.now(),
                    full_text=article_data['full_text'].strip(),
                    summary=summary
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created article: {article_data["title"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Article already exists: {article_data["title"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample articles')
        )
