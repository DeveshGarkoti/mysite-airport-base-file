# Generated by Django 5.1.1 on 2024-10-15 23:10

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('meta_title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_keywords', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('iata_code', models.CharField(max_length=3)),
                ('icao_code', models.CharField(max_length=4)),
                ('headquarters', models.CharField(max_length=255)),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Text')),
                ('operational', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3)),
                ('area_served', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('website', models.URLField(blank=True, null=True)),
                ('contact_info', models.CharField(max_length=255)),
                ('map_link', models.URLField(blank=True, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('instagram_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('youtube_url', models.URLField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='airlines/')),
                ('photo_alt', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Archived', 'Archived')], default='Draft', max_length=10)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('layout', models.CharField(choices=[('Layout One', 'Layout One'), ('Layout Two', 'Layout Two')], default='Layout One', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('meta_title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_keywords', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('iata_code', models.CharField(max_length=4)),
                ('icao_code', models.CharField(max_length=4)),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Text')),
                ('airport_type', models.CharField(choices=[('Domestic', 'Domestic'), ('International', 'International'), ('Private', 'Private')], default='Domestic', max_length=20)),
                ('operational', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3)),
                ('airport_size', models.CharField(choices=[('Big', 'Big'), ('Small', 'Small')], default='Big', max_length=10)),
                ('area_served', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('website', models.URLField(blank=True, null=True)),
                ('contact_info', models.CharField(max_length=255)),
                ('maps_link', models.URLField(blank=True, null=True)),
                ('embed_map', models.TextField(blank=True, help_text='Paste embed map code here', null=True)),
                ('embed_code', models.TextField(blank=True, help_text='Paste embed code here (e.g., for YouTube videos, interactive maps, etc.)', null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('instagram_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('youtube_url', models.URLField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='airports/')),
                ('photo_alt', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Archived', 'Archived')], default='Draft', max_length=10)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('layout', models.CharField(choices=[('Layout One', 'Layout One'), ('Layout Two', 'Layout Two')], default='Layout One', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('iso_alpha2', models.CharField(blank=True, max_length=3)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='country/')),
                ('photo_alt', models.CharField(max_length=255)),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Text')),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Text')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='facilities/')),
                ('photo_alt', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircrafts_airlines', to='AirportsDetails.airline')),
            ],
        ),
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to='AirportsDetails.airport')),
            ],
        ),
        migrations.AddField(
            model_name='airport',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AirportsDetails.country'),
        ),
        migrations.AddField(
            model_name='airline',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airlines_country', to='AirportsDetails.country'),
        ),
        migrations.AddField(
            model_name='airport',
            name='facilities_available',
            field=models.ManyToManyField(related_name='airports_facilities', to='AirportsDetails.facility'),
        ),
        migrations.AddField(
            model_name='country',
            name='faqs',
            field=models.ManyToManyField(blank=True, related_name='countries_faq', to='AirportsDetails.faq'),
        ),
        migrations.AddField(
            model_name='airport',
            name='faqs',
            field=models.ManyToManyField(blank=True, related_name='airports_faq', to='AirportsDetails.faq'),
        ),
        migrations.AddField(
            model_name='airline',
            name='faqs',
            field=models.ManyToManyField(blank=True, related_name='airlines_faq', to='AirportsDetails.faq'),
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('office', models.CharField(max_length=255)),
                ('meta_title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_keywords', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Text')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='offices/')),
                ('photo_alt', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Archived', 'Archived')], default='Draft', max_length=10)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('layout', models.CharField(choices=[('Layout One', 'Layout One'), ('Layout Two', 'Layout Two')], default='Layout One', max_length=20)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offices_airline', to='AirportsDetails.airline')),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offices_airport', to='AirportsDetails.airport')),
                ('faqs', models.ManyToManyField(blank=True, related_name='offices_faq', to='AirportsDetails.faq')),
            ],
        ),
        migrations.CreateModel(
            name='PlacesToVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('meta_title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_keywords', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Text')),
                ('embed_code', models.TextField(blank=True, help_text='Paste embed code here (e.g., for YouTube videos, interactive maps, etc.)', null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='places/')),
                ('photo_alt', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Archived', 'Archived')], default='Draft', max_length=10)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='places_countries', to='AirportsDetails.country')),
                ('faqs', models.ManyToManyField(blank=True, related_name='places_faq', to='AirportsDetails.faq')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='places_to_visit',
            field=models.ManyToManyField(blank=True, related_name='countries_places', to='AirportsDetails.placestovisit'),
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('terminal_number', models.CharField(max_length=10)),
                ('meta_title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_keywords', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Text')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='terminals/')),
                ('photo_alt', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Archived', 'Archived')], default='Draft', max_length=10)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('layout', models.CharField(choices=[('Layout One', 'Layout One'), ('Layout Two', 'Layout Two')], default='Layout One', max_length=20)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terminals_airline', to='AirportsDetails.airline')),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terminals_airport', to='AirportsDetails.airport')),
                ('faqs', models.ManyToManyField(blank=True, related_name='terminals_faq', to='AirportsDetails.faq')),
            ],
        ),
    ]
