# Generated by Django 3.1.1 on 2020-11-01 16:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0015_auto_20201101_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='requirement_type',
            field=models.IntegerField(choices=[(0, 'Remove'), (1, 'Pending'), (2, 'Doing'), (3, 'Done')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 1, 23, 15, 17, 582347)),
        ),
        migrations.AlterField(
            model_name='task',
            name='last_edit_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 1, 23, 15, 17, 582374)),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(0, 'Normality'), (1, 'Priority')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 1, 23, 15, 17, 582393)),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(choices=[(0, 'Remove'), (1, 'Pending'), (2, 'Doing'), (3, 'Done')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Not know'), (1, 'Female'), (2, 'Male'), (3, 'Other')], default=0),
        ),
    ]