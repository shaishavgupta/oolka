# Generated by Django 3.2.25 on 2024-05-22 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20240522_1129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='link',
        ),
    ]
