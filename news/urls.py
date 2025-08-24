from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('scrape/', views.scrape_articles, name='scrape_articles'),
    path('scrape/stop/', views.stop_scraping, name='stop_scraping'),
    path('api/scraping-progress/', views.scraping_progress, name='scraping_progress'),
]
