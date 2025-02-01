from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the logged-in user
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Type of the related model
    object_id = models.PositiveIntegerField()  # ID of the object being commented on
    content_object = GenericForeignKey('content_type', 'object_id')  # Generic foreign key to related model
    comment_text = models.TextField()  # Comment text
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set date when created
    updated_at = models.DateTimeField(auto_now=True)  # Auto update date when modified

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user} on {self.content_type}'
