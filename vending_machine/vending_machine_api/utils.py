from enum import IntEnum

class CoinEnum(IntEnum):

    """

    An Enumeration to define the accepted coin types for this vending machine.
    This enumeration defines GB/UK coins ONLY.

    """

    PENCE_1 = 1
    PENCE_2 = 2
    PENCE_5 = 5
    PENCE_10 = 10
    PENCE_20 = 20
    PENCE_50 = 50
    PENCE_100 = 100
    PENCE_200 = 200

    @classmethod
    def choices(cls):
        return [(coin.value, coin.name) for coin in cls]