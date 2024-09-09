# Generated by Django 5.0.6 on 2024-06-27 15:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_post_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='loves',
            field=models.ManyToManyField(blank=True, related_name='post_love', to=settings.AUTH_USER_MODEL),
        ),
    ]
