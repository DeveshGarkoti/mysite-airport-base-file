# Generated by Django 5.1.1 on 2024-10-22 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AirportsDetails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='placestovisit',
            name='embed_map',
            field=models.TextField(blank=True, help_text='Paste embed map code here', null=True),
        ),
    ]
