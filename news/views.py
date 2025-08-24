from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from .models import Article
from .scraper import scrape_news_articles, save_article_to_db
from .utils import summarize_text
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
import threading

# Global variable to track scraping status
scraping_status = {
    'is_running': False,
    'progress': 0,
    'total': 0,
    'message': 'Ready to scrape',
    'stop_requested': False
}

def get_news_statistics():
    """
    Calculate comprehensive statistics for the dashboard
    """
    # Total articles
    total_articles = Article.objects.count()
    
    # Number of sources (based on distinct domains from URLs)
    sources_count = Article.objects.values('url').distinct().count()
    if sources_count > 0:
        # Extract unique domains
        from urllib.parse import urlparse
        domains = set()
        for article in Article.objects.all():
            try:
                domain = urlparse(article.url).netloc
                if domain:
                    domains.add(domain)
            except:
                pass
        sources_count = len(domains)
    else:
        sources_count = 1  # Default to 1 as we have India Today configured
    
    # Articles with AI summaries (non-empty summary field)
    ai_summaries_count = Article.objects.filter(
        summary__isnull=False
    ).exclude(summary='').count()
    
    # Recent updates (articles from last 24 hours)
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    recent_updates_count = Article.objects.filter(
        created_at__gte=twenty_four_hours_ago
    ).count()
    
    # Latest article time for real-time updates
    latest_article = Article.objects.first()  # Already ordered by -created_at
    time_since_last_update = None
    if latest_article:
        time_diff = timezone.now() - latest_article.created_at
        if time_diff.days > 0:
            time_since_last_update = f"{time_diff.days}d ago"
        elif time_diff.seconds > 3600:
            hours = time_diff.seconds // 3600
            time_since_last_update = f"{hours}h ago"
        elif time_diff.seconds > 60:
            minutes = time_diff.seconds // 60
            time_since_last_update = f"{minutes}m ago"
        else:
            time_since_last_update = "Just now"
    else:
        time_since_last_update = "No updates"
    
    return {
        'total_articles': total_articles,
        'sources_count': sources_count,
        'ai_summaries_count': ai_summaries_count,
        'recent_updates_count': recent_updates_count,
        'time_since_last_update': time_since_last_update,
        'has_articles': total_articles > 0
    }

def home(request):
    """
    Homepage showing latest news summaries
    """
    global scraping_status
    
    # Handle scraping request from homepage
    if request.method == 'POST':
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if scraping_status['is_running']:
            message = 'Scraping is already in progress!'
            if is_ajax:
                return JsonResponse({
                    'success': False, 
                    'message': message
                })
            else:
                messages.warning(request, message)
        else:
            # Start scraping in background thread
            thread = threading.Thread(target=run_scraping_process)
            thread.daemon = True
            thread.start()
            
            message = 'Scraping started! Fresh articles will appear below.'
            if is_ajax:
                return JsonResponse({
                    'success': True, 
                    'message': message
                })
            else:
                messages.success(request, message)
    
    articles = Article.objects.all()[:10]  # Show latest 10 articles
    stats = get_news_statistics()  # Get comprehensive statistics
    
    context = {
        'articles': articles,
        'total_articles': stats['total_articles'],
        'sources_count': stats['sources_count'],
        'ai_summaries_count': stats['ai_summaries_count'],
        'recent_updates_count': stats['recent_updates_count'],
        'time_since_last_update': stats['time_since_last_update'],
        'has_articles': stats['has_articles'],
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

def stop_scraping(request):
    """
    Stop the current scraping process
    """
    global scraping_status
    
    if request.method == 'POST':
        if scraping_status['is_running']:
            scraping_status['stop_requested'] = True
            scraping_status['message'] = 'Stop requested... finishing current task'
            messages.success(request, 'Scraping stop requested. Process will finish gracefully.')
        else:
            messages.info(request, 'No scraping process is currently running.')
    
    # Redirect back to the previous page
    return_url = request.META.get('HTTP_REFERER', '/')
    from django.shortcuts import redirect
    return redirect(return_url)

def run_scraping_process():
    """
    Background function to scrape and process articles
    """
    global scraping_status
    
    scraping_status['is_running'] = True
    scraping_status['progress'] = 0
    scraping_status['stop_requested'] = False  # Reset stop flag
    scraping_status['message'] = 'Starting scraping process...'
    
    try:
        # Check if stop was requested before even starting
        if scraping_status['stop_requested']:
            scraping_status['message'] = 'Scraping stopped before starting'
            return
        
        # Scrape articles
        scraping_status['message'] = 'Scraping articles...'
        
        # Define stop check function
        def check_stop():
            return scraping_status['stop_requested']
        
        articles_data = scrape_news_articles(stop_check_func=check_stop)
        
        if not articles_data:
            scraping_status['message'] = 'No articles found'
            return
            
        # Check if stop was requested after scraping
        if scraping_status['stop_requested']:
            scraping_status['message'] = 'Scraping stopped during article collection'
            return
        
        scraping_status['total'] = len(articles_data)
        scraping_status['message'] = f'Processing {len(articles_data)} articles...'
        
        processed = 0
        for i, article_data in enumerate(articles_data):
            # Check if stop was requested before processing each article
            if scraping_status['stop_requested']:
                scraping_status['message'] = f'Scraping stopped. Processed {processed} articles before stopping.'
                break
                
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
        
        # Set completion message based on whether we were stopped or completed normally
        if scraping_status['stop_requested']:
            scraping_status['message'] = f'Scraping stopped by user. Processed {processed} new articles.'
        else:
            scraping_status['message'] = f'Completed! Processed {processed} new articles.'
        
    except Exception as e:
        scraping_status['message'] = f'Error: {str(e)}'
        print(f"Scraping error: {e}")
    
    finally:
        scraping_status['is_running'] = False
        scraping_status['stop_requested'] = False  # Reset stop flag when done
