# Generated by Django 3.0.2 on 2020-03-04 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0010_disposition_driver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disposition',
            name='disposition_type',
        ),
    ]
