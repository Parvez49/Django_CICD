# Generated by Django 5.0.6 on 2024-08-25 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_usermedia"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="receive_message",
            field=models.BooleanField(default=False),
        ),
    ]
