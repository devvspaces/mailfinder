# Generated by Django 3.1.6 on 2021-02-27 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scraper', '0006_auto_20210223_0417'),
    ]

    operations = [
        migrations.CreateModel(
            name='OdinList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(default='N/A', max_length=500)),
                ('scraped', models.BooleanField(default=False)),
                ('last_scraped', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='emailmodel',
            name='job_title',
        ),
    ]
