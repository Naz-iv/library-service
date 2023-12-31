# Generated by Django 4.2.8 on 2023-12-15 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("borrowing_service", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "pending"), ("PAID", "paid")],
                        default="PENDING",
                        max_length=40,
                    ),
                ),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("PAYMENT", "payment"), ("FINE", "fine")],
                        default="PAYMENT",
                        max_length=40,
                    ),
                ),
                ("session_url", models.URLField(blank=True, null=True)),
                ("session_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "money_to_be_paid",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "borrowing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="borrowing_service.borrowing",
                    ),
                ),
            ],
        ),
    ]
