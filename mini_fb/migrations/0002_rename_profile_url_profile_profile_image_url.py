# Generated by Django 5.1.1 on 2024-10-07 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile_url',
            new_name='profile_image_url',
        ),
    ]
