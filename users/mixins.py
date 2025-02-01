# mixins.py
from django.contrib.contenttypes.models import ContentType
from users.models import Comment
from users.forms import CommentForm

class CommentContextMixin:
    def get_comment_context(self, object):
        # Retrieve comments for the current object
        content_type = ContentType.objects.get_for_model(object)
        comments = Comment.objects.filter(content_type=content_type, object_id=object.id)

        return {
            'comments': comments,
            'content_type': content_type,
            'comment_form': CommentForm()  # Initialize the comment form
        }
