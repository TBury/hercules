# Generated by Django 3.0.2 on 2020-04-18 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hercules_app', '0045_auto_20200417_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hercules_app.Company'),
        ),
    ]
