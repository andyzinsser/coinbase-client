# Coinbase Python Client

Minimal python library for interacting with Coinbase API in python. Uses API Key+Secret authentication.

## Installation

```
git clone git@github.com:andyzinsser/coinbase-client.git
cd coinbase-client
pip install -r requirements.txt
```

## Usage

```python
from CoinbaseClient import CoinbaseClient

key = os.environ['API_KEY']
secret = os.environ['API_SECRET']
client = CoinbaseClient(API_KEY=key, API_SECRET=secret)
client.get_balance()
print client.balance
```

