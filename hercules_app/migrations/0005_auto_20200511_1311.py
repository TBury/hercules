# Generated by Django 3.0.2 on 2020-05-11 13:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0004_auto_20200509_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='registration_number',
        ),
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 11, 13, 11, 50, 803117)),
        ),
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 11, 13, 11, 50, 803117)),
        ),
    ]
