import requests
import json
import time
import hashlib
import hmac

VERSION = 'v1'
BASE_URL = 'https://coinbase.com/api/'
URLS = {
    'SEND_MONEY': '%s%s/transactions/send_money' % (BASE_URL, VERSION),
    'BALANCE': '%s%s/account/balance' % (BASE_URL, VERSION),
    'TRANSACTIONS': '%s%s/transactions' % (BASE_URL, VERSION)
}


class CoinbaseClient(object):
    """ Wrapper for the coinbase API
    """

    def __init__(self, *args, **kwargs):

        self._API_KEY = kwargs.get('API_KEY')
        self._API_SECRET = kwargs.get('API_SECRET')
        self._headers = {
            'Content-type': 'application/json',
            'ACCESS_KEY': self._API_KEY,
            'ACCESS_SIGNATURE': '',
            'ACCESS_NONCE': ''
        }

        self.balance = 0

    def __get(self, url):
        """ HTTP GET request wrapper. Sets up the headers for each request """
        self.__add_signature_to_headers(url=url)
        r = requests.get(url, headers=self._headers)
        return json.loads(r.content)

    def __post(self, url, body=None):
        body = json.dumps(body)
        self.__add_signature_to_headers(url=url, body=body)
        r = requests.post(url, data=body, headers=self._headers)
        return json.loads(r.content)

    def __add_signature_to_headers(self, url=None, body=None):
        """ Generates hmac sig with nonce + url + [body] """
        nonce = int(time.time() * 1e6)
        message = str(nonce) + url + ('' if body is None else body)
        self._headers['ACCESS_NONCE'] = nonce
        self._headers['ACCESS_SIGNATURE'] = hmac.new(self._API_SECRET, message, hashlib.sha256).hexdigest()

    def get_balance(self):
        """ https://coinbase.com/api/doc/1.0/accounts/balance.html """
        response = self.__get(URLS['BALANCE'])
        self.balance = response['amount']
        return self.balance

    def get_transactions(self):
        """ https://coinbase.com/api/doc/1.0/transactions/index.html """
        response = self.__get(URLS['TRANSACTIONS'])
        self.transactions = response['transactions']
        return self.transactions

    def send(self, to=None, amount=None):
        """ https://coinbase.com/api/doc/1.0/transactions/send_money.html """
        payload = {
            'transaction': {
                'to': to,
                'amount': amount
            }
        }
        response = self.__post(URLS['SEND_MONEY'], body=payload)
        return response['success'], response['errors']
