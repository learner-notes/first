# Generated by Django 4.0.3 on 2022-08-15 15:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpha', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=6)),
                ('countrycode', models.CharField(default='IN', max_length=10)),
                ('people', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
