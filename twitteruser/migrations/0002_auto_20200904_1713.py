# Generated by Django 3.1.1 on 2020-09-04 17:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitteruser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitteruser',
            name='following',
        ),
        migrations.AddField(
            model_name='twitteruser',
            name='following',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
