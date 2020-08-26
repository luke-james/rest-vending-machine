from django.db import models
from .utils import CoinEnum

# Create your models here.
class CoinRegister(models.Model):
    unit = models.PositiveIntegerField(verbose_name="Coin Type/Unit", choices=CoinEnum.choices(), default=CoinEnum.PENCE_1)
    count = models.PositiveIntegerField(verbose_name="Number of Coins", default=0) 

    def __str__(self):
        return CoinEnum(self.unit).name.title()

    def get_value(self):
        return CoinEnum(self.unit).value


