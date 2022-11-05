import requests
import hmac
import base64
import hashlib
import datetime
from urllib.parse import urlencode
import config

rest_url = 'https://api.example.com'
rest_path = 'api.example.com'

api_key = config.key
api_secret = config.secret

ts = datetime.datetime.utcnow().isoformat()
nonce = 123

# REST API method
method = '/v1/orders/cancel-all'
body = '{}'

msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, nonce, 'DELETE', rest_path, method, body)
sig = base64.b64encode(hmac.new(api_secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

header = {'Content-Type': 'application/json', 'AccessKey': api_key,
          'Timestamp': ts, 'Signature': sig, 'Nonce': str(nonce)}

resp = requests.delete(rest_url + method, headers=header,data=body)
print(resp.json())