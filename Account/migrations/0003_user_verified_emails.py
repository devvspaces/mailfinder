# Generated by Django 3.1.6 on 2021-02-27 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_auto_20210206_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verified_emails',
            field=models.IntegerField(default=90),
        ),
    ]