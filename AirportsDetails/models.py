from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


# Faqs
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    meta_title = models.CharField(max_length=70, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.question)
            slug = base_slug
            counter = 1
            while FAQ.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)   

    def get_absolute_url(self):
        return reverse('faq_detail', args=[self.slug])


    def __str__(self):
        return self.question


# Aircraft Model
class Aircraft(models.Model):
    title = models.CharField(max_length=255)
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE, related_name='aircrafts_airlines')

    def __str__(self):
        return self.title


# Places to Visit Model
class PlacesToVisit(models.Model):
    # Post Title
    title = models.CharField(max_length=255)
    
    # Meta Section
    meta_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()
    
    # Content Section
    content=CKEditor5Field('Text', config_name='extends', blank=True)

    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='places_countries')
    faqs = models.ManyToManyField(FAQ, related_name='places_faq', blank=True)  # Many-to-Many field for FAQs
    
    embed_map = models.TextField(blank=True, null=True, help_text="Paste embed map code here")

    embed_code = models.TextField(blank=True, null=True, help_text="Paste embed code here (e.g., for YouTube videos, interactive maps, etc.)")

    # Photo Section
    photo = models.ImageField(upload_to='places/', blank=True, null=True)
    photo_alt = models.CharField(max_length=255)
    
    # Status Section
    class Status(models.TextChoices):
        DRAFT = 'Draft', _('Draft')
        PUBLISHED = 'Published', _('Published')
        ARCHIVED = 'Archived', _('Archived')

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    
    publish_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'slug': self.slug})



# Country Model
class Country(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    iso_alpha2 = models.CharField(max_length=3, blank=True)
    photo = models.ImageField(upload_to='country/', blank=True, null=True)
    photo_alt = models.CharField(max_length=255)
    content=CKEditor5Field('Text', config_name='extends', blank=True)

    embed_map = models.TextField(blank=True, null=True, help_text="Paste embed map code here")
    
    embed_code = models.TextField(blank=True, null=True, help_text="Paste embed code here (e.g., for YouTube videos, interactive maps, etc.)")

    places_to_visit = models.ManyToManyField(PlacesToVisit, related_name='countries_places', blank=True)
    faqs = models.ManyToManyField(FAQ, related_name='countries_faq', blank=True)  # Many-to-Many field for FAQs

    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse('country_detail', kwargs={'slug': self.slug})



# Facility Section
class Facility(models.Model):
    title = models.CharField(max_length=100)
    content=CKEditor5Field('Text', config_name='extends', blank=True)

    photo = models.ImageField(upload_to='facilities/', blank=True, null=True)
    photo_alt = models.CharField(max_length=255)

    def __str__(self):
        return self.title



# Facility Section
class Service(models.Model):
    title = models.CharField(max_length=100)
    content=CKEditor5Field('Text', config_name='extends', blank=True)

    photo = models.ImageField(upload_to='services/', blank=True, null=True)
    photo_alt = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# Airport 
class Airport(models.Model):
    # Name
    title = models.CharField(max_length=255)

    # Meta Data Section
    meta_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()


    # Airport Details Section
    iata_code = models.CharField(max_length=4)
    icao_code = models.CharField(max_length=4)
    facilities_available = models.ManyToManyField(Facility, related_name='airports_facilities')
    faqs = models.ManyToManyField(FAQ, related_name='airports_faq', blank=True)  # Many-to-Many field for FAQs
    content=CKEditor5Field('Text', config_name='extends', blank=True)
    
    class AirportType(models.TextChoices):
        DOMESTIC = 'Domestic', _('Domestic')
        INTERNATIONAL = 'International', _('International')
        PRIVATE = 'Private', _('Private')

    airport_type = models.CharField(
        max_length=20,
        choices=AirportType.choices,
        default=AirportType.DOMESTIC,
    )

    class OperationalStatus(models.TextChoices):
        YES = 'Yes', _('Yes')
        NO = 'No', _('No')

    operational = models.CharField(
        max_length=3,
        choices=OperationalStatus.choices,
        default=OperationalStatus.YES,
    )

    class AirportSize(models.TextChoices):
        BIG = 'Big', _('Big')
        SMALL = 'Small', _('Small')

    airport_size = models.CharField(
        max_length=10,
        choices=AirportSize.choices,
        default=AirportSize.BIG,
    )

    area_served = models.CharField(max_length=255 )

    # Google Map Section
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    contact_info = models.CharField(max_length=255)
    maps_link = models.URLField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    # Embedding 
    embed_map = models.TextField(blank=True, null=True, help_text="Paste embed map code here")
    
    embed_code = models.TextField(blank=True, null=True, help_text="Paste embed code here (e.g., for YouTube videos, interactive maps, etc.)")

    # Social Media Links Section
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    # Photo Section
    photo = models.ImageField(upload_to='airports/', blank=True, null=True)
    photo_alt = models.CharField(max_length=255)

    # Necessary Section
    class Status(models.TextChoices):
        DRAFT = 'Draft', _('Draft')
        PUBLISHED = 'Published', _('Published')
        ARCHIVED = 'Archived', _('Archived')

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    publish_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class LayoutChoices(models.TextChoices):
        LAYOUT_ONE = 'Layout One', _('Layout One')
        LAYOUT_TWO = 'Layout Two', _('Layout Two')

    layout = models.CharField(
        max_length=20,
        choices=LayoutChoices.choices,
        default=LayoutChoices.LAYOUT_TWO,
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('airport_detail', kwargs={'slug': self.slug})



# Another name for Airport
class Alias(models.Model):
    title = models.CharField(max_length=100)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='aliases')

    def __str__(self):
        return self.title



# Ailines
class Airline(models.Model):
    # Post Title
    title = models.CharField(max_length=255)
    
    # Meta Section
    meta_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()
    
    # Airlines Details Section
    iata_code = models.CharField(max_length=3)
    icao_code = models.CharField(max_length=4)
    headquarters = models.CharField(max_length=255)
    content=CKEditor5Field('Text', config_name='extends', blank=True)
    
    class OperationalStatus(models.TextChoices):
        YES = 'Yes', _('Yes')
        NO = 'No', _('No')

    operational = models.CharField(
        max_length=3,
        choices=OperationalStatus.choices,
        default=OperationalStatus.YES,
    )
    
    area_served = models.CharField(max_length=255)
    faqs = models.ManyToManyField(FAQ, related_name='airlines_faq', blank=True)  # Many-to-Many field for FAQs
    services_available = models.ManyToManyField(Service, related_name='airlines_services', blank=True)


    # Google Map Details Section
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    contact_info = models.CharField(max_length=255)
    map_link = models.URLField(blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='airlines_country')
    
    
    embed_code = models.TextField(blank=True, null=True, help_text="Paste embed code here (e.g., for YouTube videos, interactive maps, etc.)")

    # Social Media Links Section
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    # Photo Section
    photo = models.ImageField(upload_to='airlines/', blank=True, null=True)
    photo_alt = models.CharField(max_length=255)

    # Necessary Section
    class Status(models.TextChoices):
        DRAFT = 'Draft', _('Draft')
        PUBLISHED = 'Published', _('Published')
        ARCHIVED = 'Archived', _('Archived')

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )


    publish_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class LayoutChoices(models.TextChoices):
        LAYOUT_ONE = 'Layout One', _('Layout One')
        LAYOUT_TWO = 'Layout Two', _('Layout Two')
        

    layout = models.CharField(
        max_length=20,
        choices=LayoutChoices.choices,
        default=LayoutChoices.LAYOUT_TWO,
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('airline_detail', kwargs={'slug': self.slug})




# Terminals
class Terminal(models.Model):
    # Post Title
    title = models.CharField(max_length=255)
    terminal_number = models.CharField(max_length=10)

    # Meta Data Section
    meta_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()

    # Content Section
    content=CKEditor5Field('Text', config_name='extends', blank=True)

    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='terminals_airport')
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='terminals_airline')
    faqs = models.ManyToManyField(FAQ, related_name='terminals_faq', blank=True)  # Many-to-Many field for FAQs

    # Photo Section
    photo = models.ImageField(upload_to='terminals/', blank=True, null=True)
    photo_alt = models.CharField(max_length=255)
    
    embed_code = models.TextField(blank=True, null=True, help_text="Paste embed code here (e.g., for YouTube videos, interactive maps, etc.)")

    # Necessary Section
    class Status(models.TextChoices):
        DRAFT = 'Draft', _('Draft')
        PUBLISHED = 'Published', _('Published')
        ARCHIVED = 'Archived', _('Archived')

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    publish_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class LayoutChoices(models.TextChoices):
        LAYOUT_ONE = 'Layout One', _('Layout One')
        LAYOUT_TWO = 'Layout Two', _('Layout Two')
        LAYOUT_HEADING = 'Layout Heading', _('Layout Heading')
        LAYOUT_IMAGES = 'Layout Images', _('Layout Images')
        LAYOUT_REVERSE = 'Layout Reverse', _('Layout Reverse')
        LAYOUT_FIRST_4 = 'Layout First 4', _('Layout First 4')
        LAYOUT_FIRST_5 = 'Layout First 5', _('Layout First 5')
        LAYOUT_FIRST_6 = 'Layout First 6', _('Layout First 6')
        LAYOUT_FIRST_8 = 'Layout First 8', _('Layout First 8')
        LAYOUT_FROM_2_TO_6 = 'Layout From 2 To 6', _('Layout From 2 To 6')
        LAYOUT_FROM_3_TO_7 = 'Layout From 3 To 7', _('Layout From 3 To 7')
        LAYOUT_FROM_4_TO_8 = 'Layout From 4 To 8', _('Layout From 4 To 8')
        LAYOUT_LAST_3 = 'Layout Last 3', _('Layout Last 3')
        LAYOUT_LAST_4 = 'Layout Last 4', _('Layout Last 4')
        LAYOUT_LAST_5 = 'Layout Last 5', _('Layout Last 5')
        LAYOUT_LEAVE_1 = 'Layout Leave 1', _('Layout Leave 1')
        LAYOUT_LEAVE_2 = 'Layout Leave 2', _('Layout Leave 2')
        LAYOUT_LEAVE_3 = 'Layout Leave 3', _('Layout Leave 3')
        LAYOUT_LEAVE_4 = 'Layout Leave 4', _('Layout Leave 4')
        

    layout = models.CharField(
        max_length=20,
        choices=LayoutChoices.choices,
        default=LayoutChoices.LAYOUT_ONE,
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('terminal_detail', kwargs={'slug': self.slug})



# Office
class Office(models.Model):
    # Post Title and Office Name/Number
    title = models.CharField(max_length=255)
    office = models.CharField(max_length=255)

    # Meta Data Section
    meta_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()

    # Content Section
    content=CKEditor5Field('Text', config_name='extends', blank=True)

    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='offices_airport')
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='offices_airline')
    faqs = models.ManyToManyField(FAQ, related_name='offices_faq', blank=True)  # Many-to-Many field for FAQs
    
    embed_code = models.TextField(blank=True, null=True, help_text="Paste embed code here (e.g., for YouTube videos, interactive maps, etc.)")

    # Photo Section
    photo = models.ImageField(upload_to='offices/', blank=True, null=True)
    photo_alt = models.CharField(max_length=255)
    
    
    # Necessary Section
    class Status(models.TextChoices):
        DRAFT = 'Draft', _('Draft')
        PUBLISHED = 'Published', _('Published')
        ARCHIVED = 'Archived', _('Archived')

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    publish_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class LayoutChoices(models.TextChoices):
        LAYOUT_ONE = 'Layout One', _('Layout One')
        LAYOUT_TWO = 'Layout Two', _('Layout Two')
        LAYOUT_HEADING = 'Layout Heading', _('Layout Heading')
        LAYOUT_IMAGES = 'Layout Images', _('Layout Images')
        LAYOUT_REVERSE = 'Layout Reverse', _('Layout Reverse')
        LAYOUT_FIRST_4 = 'Layout First 4', _('Layout First 4')
        LAYOUT_FIRST_5 = 'Layout First 5', _('Layout First 5')
        LAYOUT_FIRST_6 = 'Layout First 6', _('Layout First 6')
        LAYOUT_FIRST_8 = 'Layout First 8', _('Layout First 8')
        LAYOUT_FROM_2_TO_6 = 'Layout From 2 To 6', _('Layout From 2 To 6')
        LAYOUT_FROM_3_TO_7 = 'Layout From 3 To 7', _('Layout From 3 To 7')
        LAYOUT_FROM_4_TO_8 = 'Layout From 4 To 8', _('Layout From 4 To 8')
        LAYOUT_LAST_3 = 'Layout Last 3', _('Layout Last 3')
        LAYOUT_LAST_4 = 'Layout Last 4', _('Layout Last 4')
        LAYOUT_LAST_5 = 'Layout Last 5', _('Layout Last 5')
        LAYOUT_LEAVE_1 = 'Layout Leave 1', _('Layout Leave 1')
        LAYOUT_LEAVE_2 = 'Layout Leave 2', _('Layout Leave 2')
        LAYOUT_LEAVE_3 = 'Layout Leave 3', _('Layout Leave 3')
        LAYOUT_LEAVE_4 = 'Layout Leave 4', _('Layout Leave 4')
        
        
    layout = models.CharField(
        max_length=20,
        choices=LayoutChoices.choices,
        default=LayoutChoices.LAYOUT_ONE,
    )

    def __str__(self):
        return f'Office {self.office} - {self.title}'
    
    def get_absolute_url(self):
        return reverse('office_detail', kwargs={'slug': self.slug})

