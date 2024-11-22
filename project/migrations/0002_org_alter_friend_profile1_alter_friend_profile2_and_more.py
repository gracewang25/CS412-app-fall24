# Generated by Django 5.1.2 on 2024-11-22 20:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('city', models.TextField()),
                ('email_address', models.TextField()),
                ('published', models.DateTimeField(auto_now=True)),
                ('profile_image_url', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='org', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='friend',
            name='profile1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile1', to='project.org'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='profile2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile2', to='project.org'),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_items', to='project.org'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='project.org'),
        ),
        migrations.AlterField(
            model_name='statusmessage',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_messages', to='project.org'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
