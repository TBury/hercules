# Generated by Django 3.0.2 on 2020-04-11 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0030_auto_20200411_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='is_multiplayer',
            field=models.BooleanField(default=True),
        ),
    ]
