# Generated by Django 3.1.6 on 2021-02-23 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scraper', '0003_scrapedlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmodel',
            name='job_title',
            field=models.CharField(choices=[('0', 'N/A'), ('1', 'Engineer'), ('2', 'Banker'), ('3', 'Computer Engineer'), ('4', 'Teacher'), ('5', 'Lecturer'), ('6', 'Librarian'), ('7', 'Plumber'), ('8', 'Real Estate Agent'), ('9', 'Logistics'), ('10', 'Graphic Designer'), ('11', 'Web Designer'), ('12', 'Woodwork Engineer'), ('13', 'Electrical Engineer'), ('14', 'Ecotourism')], default='0', max_length=2),
        ),
    ]
