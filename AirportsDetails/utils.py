# utils.py (or any other utility module in your app)
from blog.models import Category, Post, Tag
from users.models import Comment
from django.contrib.contenttypes.models import ContentType
from users.forms import CommentForm


def add_common_context(context):
    context['sidebar_posts'] = Post.objects.filter(status='published').order_by('-publish_date')[:10]
    context['sidebar_categories'] = Category.objects.all()
    context['sidebar_tags'] = Tag.objects.all()
    return context
