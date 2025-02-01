from django.urls import path
from .views import PostListView, PostByCategoryView, PostByTagView, PostDetailView, CategoryListView, TagListView

urlpatterns = [
    # URL for listing all blog posts
    path('', PostListView.as_view(), name='post_list'),

    path('category/', CategoryListView.as_view(), name='category-list'),
    
    
    path('tags/', TagListView.as_view(), name='tag_list'),
    
    # URL for filtering posts by category
    path('category/<slug:slug>/', PostByCategoryView.as_view(), name='post_by_category'),

    # URL for filtering posts by tag
    path('tag/<slug:slug>/', PostByTagView.as_view(), name='post_by_tag'),

    # URL for viewing a single blog post
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),

]
