# Generated by Django 5.1.2 on 2024-10-21 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0004_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusmessage',
            name='image_file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
