# Generated by Django 3.1.1 on 2020-11-01 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0014_auto_20201101_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 1, 23, 9, 10, 56326)),
        ),
        migrations.AlterField(
            model_name='task',
            name='last_edit_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 1, 23, 9, 10, 56354)),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 1, 23, 9, 10, 56370)),
        ),
    ]