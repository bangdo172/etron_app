# Generated by Django 3.1.1 on 2020-10-11 10:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0010_auto_20201011_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='create_location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 11, 17, 52, 20, 891010)),
        ),
        migrations.AlterField(
            model_name='task',
            name='expire_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='last_edit_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 11, 17, 52, 20, 891037)),
        ),
        migrations.AlterField(
            model_name='task',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='organize',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='person',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 11, 17, 52, 20, 891057)),
        ),
    ]
