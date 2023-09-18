# Generated by Django 4.2.5 on 2023-09-15 19:42

from django.db import migrations, models


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
                ("fpath", models.CharField(max_length=300)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "new"),
                            ("reloaded", "reloaded"),
                            ("deleted", "deleted"),
                        ],
                        default="new",
                        max_length=8,
                    ),
                ),
            ],
        ),
    ]