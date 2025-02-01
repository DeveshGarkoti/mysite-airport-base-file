from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'publish_date', 'update_date')
    search_fields = ('title', 'meta_title', 'categories__title', 'tags__title')  # Add categories and tags here
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'categories', 'tags')  # Optional: filter by categories and tags

    # Enable filtering for many-to-many fields (categories and tags)
    filter_horizontal = ('categories', 'tags')  # Optional: shows a horizontal filter widget for M2M fields

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
