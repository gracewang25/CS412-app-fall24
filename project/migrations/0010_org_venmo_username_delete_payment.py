# Generated by Django 5.1.2 on 2024-12-09 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='venmo_username',
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]