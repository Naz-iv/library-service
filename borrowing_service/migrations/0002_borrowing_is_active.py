# Generated by Django 4.0.4 on 2023-12-14 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowing_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]