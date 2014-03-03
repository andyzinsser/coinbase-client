import unittest
import os
from CoinbaseClient import CoinbaseClient


class Tests(unittest.TestCase):

    def test_can_get_balance(self):
        key = os.environ['COINBASE_WALLET_API_KEY']
        secret = os.environ['COINBASE_WALLET_API_SECRET']
        client = CoinbaseClient(API_KEY=key, API_SECRET=secret)
        client.get_balance()
        print client.balance
        self.assertNotEqual(str(client.balance), str(0))

    def test_can_get_transactions(self):
        key = os.environ['COINBASE_WALLET_API_KEY']
        secret = os.environ['COINBASE_WALLET_API_SECRET']
        client = CoinbaseClient(API_KEY=key, API_SECRET=secret)
        client.get_transactions()
        self.assertNotEqual(len(client.transactions), 0)

    def test_can_send(self):
        key = os.environ['COINBASE_WALLET_API_KEY']
        secret = os.environ['COINBASE_WALLET_API_SECRET']
        client = CoinbaseClient(API_KEY=key, API_SECRET=secret)
        address = '1BaHFAWq166HGPA9HrbWU4Zsma3zrwHdY8'
        success, errors = client.send(to=address, amount=0.00001)
        self.assertEqual(success, True)


if __name__ == '__main__':
    unittest.main()
