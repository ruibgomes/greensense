# Generated by Django 3.2 on 2021-04-16 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0005_auto_20210415_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensorset',
            old_name='ip_adress',
            new_name='ip_address',
        ),
    ]
