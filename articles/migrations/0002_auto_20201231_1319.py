# Generated by Django 3.1.3 on 2020-12-31 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
