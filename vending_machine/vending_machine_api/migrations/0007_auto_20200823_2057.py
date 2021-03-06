# Generated by Django 3.1 on 2020-08-23 20:57

from django.db import migrations, models
import vending_machine_api.utils


class Migration(migrations.Migration):

    dependencies = [
        ('vending_machine_api', '0006_auto_20200823_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='unit',
            field=models.IntegerField(choices=[(1, 'PENCE_1'), (2, 'PENCE_2'), (5, 'PENCE_5'), (10, 'PENCE_10'), (20, 'PENCE_20'), (50, 'PENCE_50'), (100, 'PENCE_100'), (200, 'PENCE_200')], default=vending_machine_api.utils.CoinEnum['PENCE_1'], verbose_name='Coin Type/Unit'),
        ),
    ]
