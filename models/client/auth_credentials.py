from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.environ.get('APIKEY')
api_secret = os.environ.get('API_SECRET')
api_passphrase = os.environ.get('API_PASS')
api_url = os.environ.get('SANDBOX_URL')
