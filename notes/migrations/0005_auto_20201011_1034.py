# Generated by Django 3.1.1 on 2020-10-11 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_auto_20201011_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='create_time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.DateField(default=datetime.date.today),
        ),
    ]