from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = (
        'title', 'description', 'created_at',
        'updated_at', 'is_published', 'author', 'id'
        )
    list_display_links = ('title', 'description')
    search_fields = ('title', 'description', 'content', 'id', 'slug')
    list_filter = ('is_published', 'created_at', 'updated_at')
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
