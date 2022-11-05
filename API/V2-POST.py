import requests
import hmac
import base64
import hashlib
import datetime
from urllib.parse import urlencode
import config
key = config.key
secret = config.secret
# Keys
param = (
        'https://api-prod.example.com',
        'api-prod.example.com', # API
        key, # KEY
        secret, # SECRET
        123 # NONCE
)

class Post:
    def __init__(self, rest_url, rest_path, api_key, api_secret, nonce, method, body):
        self.rest_url = rest_url
        self.rest_path = rest_path
        self.api_key = api_key
        self.api_secret = api_secret
        self.nonce = nonce
        self.method = method
        self.body = body
    def makeRequest(self):
        ts = datetime.datetime.utcnow().isoformat()
        path = self.method
        body = self.body

        msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, self.nonce, 'POST', self.rest_path, path, self.body)
        sig = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

        header = {'Content-Type': 'application/json', 'AccessKey': self.api_key,
                'Timestamp': ts, 'Signature': sig, 'Nonce': str(self.nonce)}

        resp = requests.post(self.rest_url + path, headers=header, data=body)
        print(resp.content)
        #print("\nSTART @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #print("\nREQUEST URL")
        #print(resp.request.url)
        #print("\nREQUEST BODY")
        #print(resp.request.body)
        #print("\nREQUEST HEADERS")
        #print(resp.request.headers)
        #print("\nRESPONSE")
        print(resp.status_code)
        
DeliveryOrders = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2.1/delivery/orders',
        '{"instrumentId": "BTC-USD-SWAP-LIN", "qtyDeliver": "1"}'
)

PlaceOrders = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2/orders/place',
        '{"responseType":"FULL","timestamp":1615430912440,"orders":[{"clientOrderId":"496758215419","marketCode":"BTC-USD","side":"BUY","quantity":"0.001","timeInForce":"GTC","orderType":"LIMIT","price":"46017"}]}'
)

ModifyOrders = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2/orders/modify',
        '{"responseType":"FULL","timestamp":1615430912440,"orders":[{"clientOrderId":"496758215419","marketCode":"BTC-USD","side":"BUY","quantity":"0.001","timeInForce":"GTC","orderType":"LIMIT","price":"46018"}]}'
)

Mint = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2/mint',
        '{"asset": "flexUSD","quantity": 1000}'
)

Borrow = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2/borrow',
        '{"borrowAsset": "USD","collateralAsset": "BTC","collateralAmount": "0.01"}'
)

Repay = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2/repay',
        '{"repayAsset": "USD","regainAsset": "BTC","regainAmount": "0.001"}'
)

BorrowClose = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2/borrow/close',
        '{"marketCode": "BTC-USD-SWAP-LIN","price": "29633.5","quantity": "1"}'
)

AmmCreate = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2/AMM/create',
        '{"direction": "NEUTRAL","marketCode": "BTC-USD-SWAP-LIN","collateralAsset":"BTC","assetQuantity":"0.1","collateralCounterAsset":"USD","counterAssetQuantity":"4000","minPriceBound":"28000","maxPriceBound":"52000"}'
)

AmmRedeem = Post(param[0],param[1],param[2],param[3],param[4],
        '/v2/AMM/redeem',
        '{"hashToken": "CF-BTC-AMM-WJRzxzb","redeemType": "DELIVER"}'
)

# Make requests here by commenting out the request you need

#DeliveryOrders.makeRequest()
#PlaceOrders.makeRequest()
ModifyOrders.makeRequest()
#Mint.makeRequest()
#Borrow.makeRequest()
#Repay.makeRequest()
#BorrowClose.makeRequest()
#AmmCreate.makeRequest()
#AmmRedeem.makeRequest()