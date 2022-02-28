from auth import Auth
from keys import *


class Orders(Auth):
    def __init__(self, api_key, api_secret, api_passphrase, api_url):
        super().__init__(api_key, api_secret, api_passphrase, api_url)


p = Orders(api_key, api_secret, api_passphrase, api_url)
accounts = p.client.get_accounts()
for account in accounts:
    print(account)
# print(account['balance'])
# print(account[0]['id'])
# for i in account:
#     print(i)
