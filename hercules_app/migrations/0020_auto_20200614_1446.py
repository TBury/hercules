# Generated by Django 3.0.6 on 2020-06-14 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0019_auto_20200614_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 14, 14, 46, 36, 694687)),
        ),
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 14, 14, 46, 36, 694687)),
        ),
    ]
