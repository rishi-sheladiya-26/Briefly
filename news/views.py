from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from .models import Article
from .scraper import scrape_news_articles, save_article_to_db
from .utils import summarize_text
import threading

# Global variable to track scraping status
scraping_status = {
    'is_running': False,
    'progress': 0,
    'total': 0,
    'message': 'Ready to scrape'
}

def home(request):
    """
    Homepage showing latest news summaries
    """
    global scraping_status
    
    # Handle scraping request from homepage
    if request.method == 'POST':
        if scraping_status['is_running']:
            messages.warning(request, 'Scraping is already in progress!')
        else:
            # Start scraping in background thread
            thread = threading.Thread(target=run_scraping_process)
            thread.daemon = True
            thread.start()
            messages.success(request, 'Scraping started! Fresh articles will appear below.')
    
    articles = Article.objects.all()[:10]  # Show latest 10 articles
    total_articles = Article.objects.count()
    
    context = {
        'articles': articles,
        'total_articles': total_articles,
        'scraping_status': scraping_status
    }
    return render(request, 'news/home.html', context)

def article_list(request):
    """
    Paginated list of all articles
    """
    articles_list = Article.objects.all()
    paginator = Paginator(articles_list, 12)  # Show 12 articles per page
    
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    context = {
        'articles': articles,
    }
    return render(request, 'news/article_list.html', context)

def article_detail(request, pk):
    """
    Detail view for a single article
    """
    article = get_object_or_404(Article, pk=pk)
    
    context = {
        'article': article,
    }
    return render(request, 'news/article_detail.html', context)

def scrape_articles(request):
    """
    Start scraping articles in background
    """
    global scraping_status
    
    if request.method == 'POST':
        if scraping_status['is_running']:
            messages.warning(request, 'Scraping is already in progress!')
        else:
            # Start scraping in background thread
            thread = threading.Thread(target=run_scraping_process)
            thread.daemon = True
            thread.start()
            messages.success(request, 'Scraping started! Check progress below.')
    
    context = {
        'scraping_status': scraping_status
    }
    return render(request, 'news/scrape.html', context)

def scraping_progress(request):
    """
    API endpoint to get scraping progress
    """
    return JsonResponse(scraping_status)

def run_scraping_process():
    """
    Background function to scrape and process articles
    """
    global scraping_status
    
    scraping_status['is_running'] = True
    scraping_status['progress'] = 0
    scraping_status['message'] = 'Starting scraping process...'
    
    try:
        # Scrape articles
        scraping_status['message'] = 'Scraping articles...'
        articles_data = scrape_news_articles()
        
        if not articles_data:
            scraping_status['message'] = 'No articles found'
            return
        
        scraping_status['total'] = len(articles_data)
        scraping_status['message'] = f'Processing {len(articles_data)} articles...'
        
        processed = 0
        for i, article_data in enumerate(articles_data):
            try:
                scraping_status['progress'] = i + 1
                scraping_status['message'] = f'Processing article {i+1}/{len(articles_data)}...'
                
                # Check if article already exists
                if Article.objects.filter(url=article_data['url']).exists():
                    continue
                
                # Save article to database
                save_article_to_db(article_data)
                processed += 1
                
            except Exception as e:
                print(f"Error processing article: {e}")
                continue
        
        scraping_status['message'] = f'Completed! Processed {processed} new articles.'
        
    except Exception as e:
        scraping_status['message'] = f'Error: {str(e)}'
        print(f"Scraping error: {e}")
    
    finally:
        scraping_status['is_running'] = False
