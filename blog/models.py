from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse



class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    content=CKEditor5Field('Text', config_name='extends')
    categories = models.ManyToManyField(Category, related_name="posts")
    tags = models.ManyToManyField(Tag, related_name="posts")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    photo_alt_text = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    publish_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

