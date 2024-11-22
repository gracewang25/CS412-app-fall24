# Generated by Django 5.1.2 on 2024-11-22 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_org_alter_friend_profile1_alter_friend_profile2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='org',
            old_name='city',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='org',
            old_name='email_address',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='org',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='org',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='org',
            name='profile_image_url',
        ),
        migrations.AddField(
            model_name='org',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='org',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_pics/'),
        ),
    ]
