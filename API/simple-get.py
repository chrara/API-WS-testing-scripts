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
method = '/v2/orders/'

# Not required for /v2/orders
body = urlencode({})

if body:
    path = method + '?' + body
else:
    path = method

msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, nonce, 'GET', rest_path, method, body)
sig = base64.b64encode(hmac.new(secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

header = {'Content-Type': 'application/json', 'AccessKey': key,
          'Timestamp': ts, 'Signature': sig, 'Nonce': str(nonce)}

i = 1
while i <= 300:
        resp = requests.get(rest_url + method + '?')
        resp = requests.get(rest_url + method, headers=header)
        if(resp.status_code != 200):
                print("\nSTART @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                print("\nREQUEST URL")
                print(resp.request.url)
                print("\nREQUEST BODY")
                print(resp.request.body)
                print("\nREQUEST HEADERS")
                print(resp.request.headers)
                print("\nRESPONSE")
                print(resp.status_code)
                print(resp.headers)
                print(resp.content)
                i += 1
        else:
                print(resp.status_code)
                print(resp.content)