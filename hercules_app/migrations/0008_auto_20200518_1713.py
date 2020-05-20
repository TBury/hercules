# Generated by Django 3.0.2 on 2020-05-18 17:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0007_auto_20200518_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='workapplications',
            name='reject_reason',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 18, 17, 13, 38, 291414)),
        ),
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 18, 17, 13, 38, 291414)),
        ),
    ]