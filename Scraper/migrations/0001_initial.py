# Generated by Django 3.1.6 on 2021-02-28 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OdinList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.URLField(default='N/A', max_length=500, unique=True)),
                ('scraped', models.BooleanField(default=False)),
                ('last_scraped', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(default='N/A', max_length=500)),
                ('last_scraped', models.DateTimeField(auto_now=True)),
                ('beta_searched', models.BooleanField(default=False)),
                ('parent_link', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Scraper.odinlist')),
            ],
        ),
        migrations.CreateModel(
            name='EmailModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(default='N/A', max_length=225)),
                ('domain', models.URLField(default='N/A', max_length=225)),
                ('verified', models.BooleanField(default=False)),
                ('position', models.CharField(default='N/A', max_length=225)),
                ('country', models.CharField(default='N/A', max_length=225)),
                ('last_validated', models.DateTimeField(auto_now=True)),
                ('company_names', models.ManyToManyField(to='Scraper.Company')),
            ],
        ),
    ]
