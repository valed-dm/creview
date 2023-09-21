# Generated by Django 4.2.5 on 2023-09-19 16:57

from django.db import migrations, models
import files.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_name", models.CharField(max_length=50)),
                ("file", models.FileField(upload_to=files.models.user_directory_path)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(default="new", max_length=8)),
            ],
        ),
    ]
