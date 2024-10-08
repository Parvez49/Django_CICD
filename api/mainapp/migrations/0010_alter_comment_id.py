# Generated by Django 5.0.6 on 2024-07-01 19:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0009_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="id",
            field=models.CharField(
                default=uuid.uuid4,
                editable=False,
                max_length=100,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
