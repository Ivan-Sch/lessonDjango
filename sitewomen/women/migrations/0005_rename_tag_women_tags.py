# Generated by Django 4.2.1 on 2024-10-10 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0004_tagpost_alter_women_cat_women_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='women',
            old_name='tag',
            new_name='tags',
        ),
    ]