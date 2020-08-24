from django.test import TestCase, RequestFactory

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
        self.factory = RequestFactory()

    def test_empty_post_init(self):
        request = self.factory.post('/init/')
        view = MachineView()
        view.setup(request)

    def test_negative_post_init(self):
        request = self.factory.post('/init/')
        view = MachineView()
        view.setup(request)

    def test_bad_coin_type_init(self):
        request = self.factory.post('/init/')
        view = MachineView()
        view.setup(request)

    def test_good_coin_type_init(self):
        request = self.factory.post('/init/')
        view = MachineView()
        view.setup(request)

    def test_multiple_coins_init(self):
        request = self.factory.post('/init/')
        view = MachineView()
        view.setup(request)

class ChangeViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_empty_get_change(self):
        request = self.factory.get('/change/')
        view = MachineView()
        view.setup(request)

    def test_negative_get_change(self):
        request = self.factory.get('/change/')
        view = MachineView()
        view.setup(request)

    def test_bad_query_get_change(self):
        request = self.factory.get('/change/')
        view = MachineView()
        view.setup(request)

    def test_multiple_queries_get_change(self):
        request = self.factory.get('/change/')
        view = MachineView()
        view.setup(request)

    def test_positive_value_get_change(self):
        request = self.factory.get('/change/')
        view = MachineView()
        view.setup(request)

    def test_bad_type_value_get_change(self):
        request = self.factory.get('/change/')
        view = MachineView()
        view.setup(request)

    def test_empty_post_change(self):
        request = self.factory.post('/change/')
        view = MachineView()
        view.setup(request)

    def test_negative_post_change(self):
        request = self.factory.post('/change/')
        view = MachineView()
        view.setup(request)

    def test_bad_coin_type_post_change(self):
        request = self.factory.post('/change/')
        view = MachineView()
        view.setup(request)

    def test_positive_value_post_change(self):
        request = self.factory.post('/change/')
        view = MachineView()
        view.setup(request)

    def test_multiple_coins_post_change(self):
        request = self.factory.post('/change/')
        view = MachineView()
        view.setup(request)
        