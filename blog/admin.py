from django.contrib import admin
from .models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'created_at',
        'updated_at', 'is_plublished', 'author'
        )
    list_display_links = ('title', 'description')
    search_fields = ('title', 'description', 'content', 'id', 'slug')
    list_filter = ('is_plublished', 'created_at', 'updated_at')
    list_per_page = 10
    list_editable = ('is_plublished',)
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}
