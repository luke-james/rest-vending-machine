# Generated by Django 3.1 on 2020-08-23 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vending_machine_api', '0002_cointwo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CoinTwo',
        ),
        migrations.AddField(
            model_name='coin',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coin',
            name='name',
            field=models.CharField(default='', max_length=3),
        ),
    ]
