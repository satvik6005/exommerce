# Generated by Django 4.2.5 on 2023-09-06 06:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0013_alter_order_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 6, 6, 39, 12, 633501, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
