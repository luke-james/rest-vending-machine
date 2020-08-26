from enum import IntEnum
from collections import OrderedDict
from json import JSONDecoder

class UniqueDecoder():
    
    def is_collection_unique(self, deposit_pairs):
        
        unique_collection = dict()
        for key, value in deposit_pairs:
            if key in unique_collection:
                return False
            else:
                unique_collection[key] = deposit_pairs[key]
                continue

        return True

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