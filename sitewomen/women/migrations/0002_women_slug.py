# Generated by Django 4.2.1 on 2024-10-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255),
        ),
    ]
