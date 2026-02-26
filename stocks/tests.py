from django.test import TestCase, Client
from django.urls import reverse
from .utils import normalize_stock_code

class StockTest(TestCase):
    def test_normalize_stock_code(self):
        self.assertEqual(normalize_stock_code("7203"), "7203.T")
        self.assertEqual(normalize_stock_code("7203.T"), "7203.T")
        self.assertEqual(normalize_stock_code(" 7203 "), "7203.T")
        self.assertEqual(normalize_stock_code("AAPL"), "AAPL")

    def test_index_view_load(self):
        client = Client()
        response = client.get(reverse('stocks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "日本株 配当利回りグラフ")

    def test_search_invalid_code(self):
        # Testing with a known invalid code
        client = Client()
        response = client.get(reverse('stocks:index'), {'code': 'NOT_A_STOCK_CODE_123456789'})
        self.assertEqual(response.status_code, 200)
        # The exact error message depends on yfinance response, but it should contain the error div
        self.assertContains(response, "error-container")
