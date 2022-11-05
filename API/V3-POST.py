# POST
#Delivery - POST /v3/deliver
#Place order - POST /v3/orders/place
#flexAsset mint - POST /v3/flexasset/mint
#flexAsset redeem - POST /v3/flexasset/redeem
#Withdrawal request - POST /v3/withdrawal	
#Create AMM - POST /v3/AMM/new
#Redeem AMM - POST /v3/AMM/redeem
#Sub-account balance transfer - POST /v3/transfer

# DELETE
#Cancel order by ID - DELETE /v3/orders/cancel
#Cancel ALL orders - DELETE /v3/orders/cancel-all

#/v3/deliver
#/v3/orders/place
#/v3/orders/modify
#/v3/flexasset/mint
#/v3/flexasset/redeem
#/v3/withdrawal	
#/v3/AMM/new
#/v3/AMM/redeem
#/v3/transfer

#/v3/orders/cancel
#/v3/orders/cancel-all

import requests
import hmac
import base64
import hashlib
import datetime
import time
from urllib.parse import urlencode
import config
from urllib.parse import urljoin
import wfuzz
import config
from concurrent.futures import ThreadPoolExecutor
key = config.key
secret = config.secret
ddos=0
simp=1
# Keys
param = (
        'https://api.example.com',
        'api.example.com', # API
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

        proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, self.nonce, 'POST', self.rest_path, path, self.body)
        sig = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

        header = {'Content-Type': 'application/json', 'AccessKey': self.api_key,
                'Timestamp': ts, 'Signature': sig, 'Nonce': str(self.nonce)}

        
        if(simp==1):
                resp = requests.post(self.rest_url + path, headers=header, proxies=proxies, data=body, verify=False)
                print(resp.status_code, end=" ")
                print(resp.request.path_url)
                print (ts)
                print(resp.json())

        if(ddos==1):
                i = 1
                x = 0
                url = "https://" + self.rest_url + self.method + '?'+ body
                while i <= 2:
                        i += 1
                        #time.sleep(1) # give chance to catch up
                        def get_url(url):
                                return requests.post(self.rest_url + path, headers=header, data=body, proxies=proxies, verify=False )
                        list_of_urls = [url]*10
                        with ThreadPoolExecutor(max_workers=1000) as pool:
                                response_list = list(pool.map(get_url,list_of_urls))
                        for response in response_list:
                                x += 1
                                print(response.status_code, end=" ")
                                print(x)

Delivery = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/delivery',
        '{"marketCode": "BTC-USD-SWAP-LIN", "deliveryQuantity": "1"}'
)

PlaceOrders = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/orders/place',
        '{"responseType":"FULL","timestamp":"1652429539","recvWindow":50000,"orders":[{"marketCode":"BTC-USD","side":"BUY","quantity":"0.001","timeInForce":"GTC","orderType":"LIMIT","price":"30017"}]}'
)

ModifyOrders = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/orders/modify',
        '{"responseType":"FULL","timestamp":1634726937000,"orders":[{"clientOrderId":"496758215419","marketCode":"BTC-USD","side":"BUY","quantity":"0.001","timeInForce":"GTC","orderType":"LIMIT","price":"46017"}]}'
)

Mint = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/flexasset/mint',
        '{"asset": "flexUSD","quantity": 100}'
)

Redeem = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/flexasset/redeem',
        '{"asset": "flexUSD","quantity": 100, "type": "normal"}'
)

Withdraw = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/withdrawal',
        '{"asset": "FLEX", "network":"SEP20", "address":"0x963bF545F3FB75Ae03c3C4bA369cC2501309627F","memo":"642694646","quantity": 10,"externalFee":true,"tfaType": "GOOGLE","code": 076130}'

)

Transfer = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/transfer',
        '{ "asset": "BTC", "quantity": 0.0001, "fromAccount":"10516", "toAccount":"14490"}'
       

)

AmmCreate = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/AMM/create',
        '{"leverage": 1,"direction": "BUY","marketCode": "BCH-USD-SWAP-LIN","collateralAsset": "BCH","collateralQuantity": "50","minPriceBound": "200","maxPriceBound": "800"}'
)



AmmRedeem = Post(param[0],param[1],param[2],param[3],param[4],
        '/v3/AMM/redeem',
        '{"hashToken": "CF-BTC-AMM-WJRzxzb","redeemType": "DELIVER"}'
)

# Uncomment to make request

#Delivery.makeRequest() # {'success': False, 'code': '05004', 'message': 'Operation failed, please try again'}
PlaceOrders.makeRequest() # recvWindow is expired
#ModifyOrders.makeRequest() # recvWindow is expired
#Mint.makeRequest()
#Redeem.makeRequest() # Parameters of the abnormal
#Transfer.makeRequest()
#Withdraw.makeRequest()
#AmmCreate.makeRequest()
#AmmRedeem.makeRequest()