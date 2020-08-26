# Generated by Django 3.1 on 2020-08-23 20:45

from django.db import migrations, models
import vending_machine_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('vending_machine_api', '0004_auto_20200823_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='unit',
            field=models.PositiveIntegerField(choices=[(vending_machine_api.models.CoinEnum['PENCE_1'], 1), (vending_machine_api.models.CoinEnum['PENCE_2'], 2), (vending_machine_api.models.CoinEnum['PENCE_5'], 5), (vending_machine_api.models.CoinEnum['PENCE_10'], 10), (vending_machine_api.models.CoinEnum['PENCE_20'], 20), (vending_machine_api.models.CoinEnum['PENCE_50'], 50), (vending_machine_api.models.CoinEnum['PENCE_100'], 100), (vending_machine_api.models.CoinEnum['PENCE_200'], 200)], verbose_name='Coin Type/Unit'),
        ),
    ]
