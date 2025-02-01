from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from .utils import add_common_context  # Import the utility function
from users.models import Comment
from django.contrib.contenttypes.models import ContentType
from users.forms import CommentForm
from users.mixins import CommentContextMixin


# View to list all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-publish_date']
    paginate_by = 20  # Optional: Pagination (5 posts per page)

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-publish_date')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        
        context = add_common_context(context)  # Add common context

        return context

    


# View to display posts filtered by category
class PostByCategoryView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Post.objects.filter(categories=category, status='published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        
        
        context = add_common_context(context)  # Add common context

        return context


# View to display posts filtered by tag
class PostByTagView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return Post.objects.filter(tags=tag, status='published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
    
        context = add_common_context(context)  # Add common context

        return context



# View to display a single blog post
class PostDetailView(CommentContextMixin,DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')

     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = add_common_context(context)  # Add common context
        
        context['object_id'] = self.object.id
        # Add comment-related context
        context.update(self.get_comment_context(self.object))


        return context


# Class-based view for the category list
class CategoryListView(ListView):

    model = Category
    template_name = 'categories/category_list.html'  # Specify the template
    context_object_name = 'categories'  # Name for the category list in the template
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = add_common_context(context)  # Add common context

        return context
    

    
# Class-based view for the category list
class TagListView(ListView):

    model = Tag
    template_name = 'tags/tag_list.html'  # Specify the template
    context_object_name = 'tags'  # Name for the category list in the template
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = add_common_context(context)  # Add common context

        return context
    
    