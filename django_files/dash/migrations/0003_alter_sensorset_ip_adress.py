# Generated by Django 3.2 on 2021-04-14 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0002_auto_20210414_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorset',
            name='ip_adress',
            field=models.CharField(max_length=30),
        ),
    ]