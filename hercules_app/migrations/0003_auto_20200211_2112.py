# Generated by Django 3.0.2 on 2020-02-11 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0002_auto_20200211_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='last_login',
        ),
    ]
