# Generated by Django 3.0.6 on 2020-06-14 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0021_auto_20200614_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 14, 15, 13, 40, 41421)),
        ),
        migrations.AlterField(
            model_name='companysettings',
            name='periodic_norm_start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 14, 15, 13, 40, 41421)),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='loading_country',
            field=models.CharField(default='no_country', max_length=64),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='loading_spedition',
            field=models.CharField(default='no_company', max_length=100),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='unloading_country',
            field=models.CharField(default='no_country', max_length=64),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='unloading_spedition',
            field=models.CharField(default='no_company', max_length=100),
        ),
        migrations.AlterField(
            model_name='gielda',
            name='loading_country',
            field=models.CharField(default='no_country', max_length=64),
        ),
        migrations.AlterField(
            model_name='gielda',
            name='loading_spedition',
            field=models.CharField(default='no_company', max_length=100),
        ),
        migrations.AlterField(
            model_name='gielda',
            name='unloading_country',
            field=models.CharField(default='no_country', max_length=64),
        ),
        migrations.AlterField(
            model_name='gielda',
            name='unloading_spedition',
            field=models.CharField(default='no_company', max_length=100),
        ),
    ]
