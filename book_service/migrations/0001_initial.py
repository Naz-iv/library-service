# Generated by Django 4.2.8 on 2023-12-15 14:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                (
                    "cover",
                    models.CharField(
                        choices=[("hard", "HARD"), ("soft", "SOFT")],
                        default="hard",
                        max_length=5,
                    ),
                ),
                (
                    "inventory",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("daily_fee", models.DecimalField(decimal_places=2, max_digits=1000)),
            ],
            options={
                "ordering": ["title", "author", "-inventory"],
                "unique_together": {("title", "author", "cover")},
            },
        ),
    ]
