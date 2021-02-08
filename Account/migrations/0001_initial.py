# Generated by Django 3.1.6 on 2021-02-06 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=225)),
                ('last_name', models.CharField(max_length=225)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], max_length=1)),
                ('country', models.CharField(max_length=225)),
                ('active', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(auto_now=True)),
                ('disabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'MailFinder User',
            },
        ),
    ]
