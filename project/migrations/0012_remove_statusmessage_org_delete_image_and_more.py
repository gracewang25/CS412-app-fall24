# Generated by Django 5.1.2 on 2024-12-10 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_inventoryitem_image_inventoryitem_prop_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statusmessage',
            name='org',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='StatusMessage',
        ),
    ]