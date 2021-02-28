# Generated by Django 3.1.6 on 2021-02-27 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scraper', '0007_auto_20210227_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='emailmodel',
            name='company_names',
            field=models.ManyToManyField(to='Scraper.Company'),
        ),
    ]