import cbpro
from auth_credentials import api_key, api_secret, api_passphrase, api_url


class Auth():

    def __init__(self, api_key, api_secret, api_passphrase, api_url, client=None):
        print('Initiating Auth class')
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.api_url = api_url
        self.client = client
        self.auth_init()

    def auth_init(self):
        client = cbpro.AuthenticatedClient(
            self.api_key, self.api_secret, self.api_passphrase, self.api_url)
        self.client = client
        return client

# https://github.com/danpaquin/coinbasepro-python
# print(p.sell(price='200.00',  # USD
#              size='0.01',  # BTC
#              order_type='limit',
#              product_id='BTC-USD'))
# auth_client.get_account_history
