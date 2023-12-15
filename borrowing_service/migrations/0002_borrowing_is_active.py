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
