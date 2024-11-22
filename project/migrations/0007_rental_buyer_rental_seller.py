# Generated by Django 5.1.2 on 2024-11-22 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_rename_profile_statusmessage_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items_bought', to='project.org'),
        ),
        migrations.AddField(
            model_name='rental',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items_sold', to='project.org'),
            preserve_default=False,
        ),
    ]
