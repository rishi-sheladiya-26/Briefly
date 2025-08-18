from django.db import models
from django.urls import reverse
from django.utils import timezone

class Article(models.Model):
    """
    Model to store news articles with their summaries
    """
    title = models.CharField(max_length=500, blank=True, null=True)
    url = models.URLField(unique=True, max_length=1000)
    category = models.CharField(max_length=100, blank=True, null=True)
    publication_date = models.DateTimeField(blank=True, null=True)
    full_text = models.TextField()
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    
    def __str__(self):
        return self.title or f"Article from {self.url}"
    
    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'pk': self.pk})
    
    def get_short_summary(self, length=200):
        """Return a shortened version of the summary"""
        if self.summary:
            return self.summary[:length] + '...' if len(self.summary) > length else self.summary
        return self.full_text[:length] + '...' if len(self.full_text) > length else self.full_text
