# Generated by Django 3.1 on 2020-08-23 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vending_machine_api', '0007_auto_20200823_2057'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Coin',
            new_name='CoinWallet',
        ),
    ]
