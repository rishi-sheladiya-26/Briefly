from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publication_date', 'created_at']
    list_filter = ['category', 'publication_date', 'created_at']
    search_fields = ['title', 'summary', 'url']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'url', 'category', 'publication_date')
        }),
        ('Content', {
            'fields': ('summary', 'full_text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
