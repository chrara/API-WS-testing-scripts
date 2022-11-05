import requests
import hmac
import base64
import hashlib
import datetime
import config
from urllib.parse import urlencode

rest_url = 'https://api.example.com'
rest_path = 'api.example.com'

key = config.key
secret = config.secret
# Keys
param = (
        'api.example.com', # API
        key, # KEY
        secret, # SECRET
        123 # NONCE
)

ts = datetime.datetime.utcnow().isoformat()
nonce = 123

# REST API method
method = '/v2.1/delivery/orders' 

# Required for POST /v2.1/delivery/orders
body = urlencode({"instrumentId": "BTC-USD-SWAP-LIN", "qtyDeliver": "1"})

if body:
    path = method + '?' + body
else:
    path = method

msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, nonce, 'POST', rest_path, method, body)
sig = base64.b64encode(hmac.new(api_secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

header = {'Content-Type': 'application/json', 'AccessKey': api_key,
          'Timestamp': ts, 'Signature': sig, 'Nonce': str(nonce)}

resp = requests.post(rest_url + path, headers=header)
print(resp.json())