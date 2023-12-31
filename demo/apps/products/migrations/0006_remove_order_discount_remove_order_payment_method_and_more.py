# Generated by Django 4.2.4 on 2023-08-17 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_user_managers_remove_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='taxes',
        ),
        migrations.AddField(
            model_name='order',
            name='order_placed',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 17, 9, 27, 1, 30228, tzinfo=datetime.timezone.utc)),
        ),
    ]
