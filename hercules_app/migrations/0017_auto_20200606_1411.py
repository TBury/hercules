# Generated by Django 3.0.6 on 2020-06-06 14:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0016_auto_20200605_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 14, 11, 50, 324945)),
        ),
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 14, 11, 50, 324945)),
        ),
    ]
