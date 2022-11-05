import code
from crypt import methods
from math import nan
import requests
import hmac
import base64
import hashlib
import datetime
import time
from urllib.parse import urlencode
import os
from urllib.parse import urljoin
import wfuzz
import config
from concurrent.futures import ThreadPoolExecutor

#env="stage"
env="stage"

if(env == "prod"):
        key = config.prodkey
        secret = config.prodsecret
        env = 'api-prod.example.com'
else:
        key = config.key
        secret = config.secret
        env = 'api.example.com'

# Keys
param = (
        'https://api.example.com',
        env,
        key, # KEY
        secret, # SECRET
        123 # NONCE
)

simpleReq=1
ddos=0
sqlInject=0
wordlistPath="../../../Tools/Payloads/wordlist"
wordlistFile="/Injections/All_attack.txt"

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
        ts = str(datetime.datetime.utcnow().isoformat())
        path = self.method
        body = self.body

        msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, self.nonce, 'POST', self.rest_path, path, self.body)
        sig = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
        proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        header = {'Content-Type': 'application/json', 'AccessKey': self.api_key, 'User-Agent' : 'test7',
                'Timestamp': ts, 'Signature': sig, 'Nonce': str(self.nonce)}

        #############################################
        if(simpleReq==1):
                #resp = requests.post("https://" + self.rest_url + self.method + '?'+ body, headers=header, proxies=proxies, verify=False )
                resp = requests.post(self.rest_url + path, headers=header, proxies=proxies, data=body, verify=False)
                print(resp.status_code, end=" ")
                print(resp.request.path_url)
                #print(resp.json())
        if(ddos==1):
                i = 1
                x = 0
                url = "https://" + self.rest_url + self.method + '?'+ body
                while i <= 10:
                        i += 1
                        #time.sleep(1) # give chance to catch up
                        def post_url(url):
                                return requests.post(url, headers=header, proxies=proxies, verify=False )
                        list_of_urls = [url]*1000
                        with ThreadPoolExecutor(max_workers=1000) as pool:
                                response_list = list(pool.map(post_url,list_of_urls))
                        for response in response_list:
                                x += 1
                                print(response.status_code, end=" ")
                                print(x)

        if(sqlInject==1):
                for r in wfuzz.fuzz(
                        url="https://" + self.rest_url + self.method + '?'+ 'marketCode=FUZZ&asset=&hashToken=&subAcc=&timeframe=3600&limit=&startTime=&endTime=', 
                        #printer=("path","raw"), 
                        headers=[
                        ('Connection', 'keep-alive'),
                        ('Content-Type', 'application/json'),
                        ('AccessKey', self.api_key),
                        ('User-Agent', 'test11'),
                        ('Timestamp', ts),
                        ('Signature', sig),
                        ('Nonce', str(self.nonce))],
                        method="POST",
                        concurrent=5,
                        #scanmode=True,
                        delay=0.5,
                        #sc=[200],
                        proxies=[("127.0.0.1",8080,"HTTP")],
                        payloads=[("file",dict(fn=wordlistPath+wordlistFile))]):
                                print("-------------------------------------------------------------------")
                                print (r.history.code, end=" ")
                                print("PATH: " + str(r.history.params.get))
                                print("-------------------------------------------------------------------")

#############################################################################################################
# docs.coinflex.com V3 PRIVATE (auth required)
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

Delivery.makeRequest() # {'success': False, 'code': '05004', 'message': 'Operation failed, please try again'}
PlaceOrders.makeRequest() # recvWindow is expired
ModifyOrders.makeRequest() # recvWindow is expired
Mint.makeRequest()
Redeem.makeRequest() # Parameters of the abnormal
#Transfer.makeRequest()
#Withdraw.makeRequest()
#AmmCreate.makeRequest()
#AmmRedeem.makeRequest()