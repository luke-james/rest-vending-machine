from django.test import TestCase, RequestFactory, Client
import json

# utils
from .utils import CoinEnum

# models 
from .models import CoinWallet

# views
from .views import MachineView
from .views import ChangeView

class CoinWalletTestCase(TestCase):
    def setUp(self):
        CoinWallet.objects.create(unit=CoinEnum['PENCE_1'])
        CoinWallet.objects.create(unit=CoinEnum['PENCE_200'])

    def test_CoinTypeCount(self):

        coin_type_1 = CoinWallet.objects.get(unit=CoinEnum['PENCE_1'])
        self.assertEquals(coin_type_1.get_value(), 1)

        coin_type_2 = CoinWallet.objects.get(unit=CoinEnum['PENCE_200'])
        self.assertEquals(coin_type_2.get_value(), 200)


class MachineViewTestCase(TestCase):
    def setUp(self):
        self.url = '/init/'
        self.client = Client()

    def test_empty_post_init(self):

        """
        Initialization of no coins.
        """

        data = {

        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 200)

    def test_negative_post_init(self):
        
        """
        Initialization of a negative number of a type of coins.
        """

        data = {
            "PENCE_1": -1
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 406)

    def test_bad_coin_type_init(self):

        """
        Initialization of a invalid type of coin.
        """

        data = {
            "PENCE_INVALID": 1
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 406)

    def test_good_coin_type_init(self):

        """
        Initialization of a valid number of valid type of coins.
        """

        data = {
            "PENCE_1": 10
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 200)

class WithdrawChangeViewTestCase(TestCase):
    def setUp(self):
        self.url = '/change/'
        self.client = Client()

        CoinWallet.objects.create(unit=CoinEnum['PENCE_1'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_2'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_5'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_10'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_20'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_50'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_100'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_200'], count=2)
    
    def tearDown(self):
        CoinWallet.objects.all().delete()

    def test_positive_value_get_change(self):

        """
        Test the withdrawl of a single, valid coin that exists.
        """

        response = self.client.get(self.url, { "amount": 1 })
        self.assertEqual(response.status_code, 200)
    
    def test_positive_too_much_value_get_change(self):

        """
        Test the withdrawl of a value greater than the amount available in the machine.
        """

        response = self.client.get(self.url, { "amount": 10001 })
        self.assertEqual(response.status_code, 206)

    def test_empty_get_change(self):

        """
        Test the request for a withdrawl with no query parameters sent as part of the request.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_negative_get_change(self):
           
        """
        Test the withdrawl of a negative amount of coins.
        """
    
        response = self.client.get(self.url, { "amount": -1 })
        self.assertEqual(response.status_code, 400)

    def test_bad_query_get_change(self):

        """
        Test the request for a withdrawl with an query parameter sent as part of the request.
        """

        response = self.client.get(self.url, { "invalid_query": -1 })
        self.assertEqual(response.status_code, 400)

    def test_string_value_get_change(self):

        """
        Test the request for a number of coins expressed as a string.
        """

        response = self.client.get(self.url, { "amount": "100" })
        self.assertEqual(response.status_code, 200)

    def test_float_whole_value_get_change(self):

        """
        Test the request for a number of coins expressed as a 'whole' float.
        """

        response = self.client.get(self.url, { "amount": 2.0 })
        self.assertEqual(response.status_code, 400)
    
    def test_float_non_whole_value_get_change(self):
        
        """
        Test the request for a number of coins expressed as a 'non-whole' float.
        """

        response = self.client.get(self.url, { "amount": 2.5 })
        self.assertEqual(response.status_code, 400)

class DepositChangeViewTestCase(TestCase):
    def setUp(self):
        self.url = '/change/'
        self.client = Client()

        CoinWallet.objects.create(unit=CoinEnum['PENCE_1'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_2'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_5'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_10'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_20'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_50'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_100'], count=2)
        CoinWallet.objects.create(unit=CoinEnum['PENCE_200'], count=2)
    
    def tearDown(self):
        CoinWallet.objects.all().delete() 


    def test_positive_value_post_change(self):

        """
        Test the deposit of cash (no cash given).
        """

        data = {
            "PENCE_1": 1
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 200)

    def test_empty_post_change(self):    

        """
        Test the deposit of cash (no cash given).
        """

        data = {

        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 304)

    def test_negative_post_change(self):
        
        """
        Test the deposit of cash (negative amount of coin type given).
        """

        data = {
            "PENCE_1": -1
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 400)

    def test_bad_coin_type_post_change(self):
        
        """
        Test the deposit of cash (negative amount of coin type given).
        """

        data = {
            "INVALID_COIN_TYPE": 1
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 400)

    def test_string_value_post_change(self):
        
        """
        Test the deposit of cash (string type given for coin count).
        """

        data = {
            "PENCE_1": "1"
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 400)

    def test_float_whole_value_post_change(self):
        
        """
        Test the deposit of cash (float type given for coin count).
        """

        data = {
            "INVALID_COIN_TYPE": 1.0
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 400)

    def test_float_non_whole_value_post_change(self):
        
        """
        Test the deposit of cash (float type given for coin count).
        """

        data = {
            "PENCE_1": 1.5
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='text/json')
        self.assertEqual(response.status_code, 400)
