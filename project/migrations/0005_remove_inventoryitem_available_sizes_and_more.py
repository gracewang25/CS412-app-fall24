# Generated by Django 5.1.2 on 2024-11-22 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_remove_friend_profile1_remove_friend_profile2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryitem',
            name='available_sizes',
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='size_l',
            field=models.PositiveIntegerField(default=0, verbose_name='Large Quantity'),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='size_m',
            field=models.PositiveIntegerField(default=0, verbose_name='Medium Quantity'),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='size_s',
            field=models.PositiveIntegerField(default=0, verbose_name='Small Quantity'),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='size_xl',
            field=models.PositiveIntegerField(default=0, verbose_name='Extra Large Quantity'),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='size_xs',
            field=models.PositiveIntegerField(default=0, verbose_name='Extra Small Quantity'),
        ),
    ]
