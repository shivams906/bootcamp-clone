# Generated by Django 3.1.3 on 2020-12-09 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_feed_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feed',
            options={'ordering': ['-created_at']},
        ),
    ]