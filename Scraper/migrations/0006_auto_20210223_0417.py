# Generated by Django 3.1.6 on 2021-02-23 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scraper', '0005_auto_20210223_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapedlink',
            name='link',
            field=models.URLField(default='N/A', max_length=500),
        ),
    ]
