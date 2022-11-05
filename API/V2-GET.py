import requests
import hmac
import base64
import hashlib
import datetime
import config
from urllib.parse import urlencode

key = config.key
secret = config.secret
# Keys
param = (
        'api.example.com', # API
        key, # KEY
        secret, # SECRET
        123 # NONCE
)

class Get:
    def __init__(self,rest_url,api_key,api_secret,nonce,method):
        self.rest_url = rest_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.nonce = nonce
        self.method = method
    def makeRequest(self):
        ts = datetime.datetime.utcnow().isoformat()
        body = ""
        msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, self.nonce, 'GET', self.rest_url, self.method, body)
        sig = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

        header = {'Content-Type': 'application/json', 'AccessKey': self.api_key,
                'Timestamp': ts, 'Signature': sig, 'Nonce': str(self.nonce)}

        resp = requests.get("https://" + self.rest_url + self.method + '?', headers=header)
        #print(resp.json())
        #print("\nSTART @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #print("\nREQUEST URL")
        #print(resp.request.url)
        #print("\nREQUEST BODY")
        #print(resp.request.body)
        #print("\nREQUEST HEADERS")
        #print(resp.request.headers)
        #print("\nRESPONSE")
        print(resp.status_code)

AccountInfo = Get(param[0],param[1],param[2],param[3],"/v2/accountinfo")
Balance = Get(param[0],param[1],param[2],param[3],"/v2/balances")
BalanceId = Get(param[0],param[1],param[2],param[3],"/v2/balances/FLEX")
Postitions = Get(param[0],param[1],param[2],param[3],"/v2/positions")
PostitionsId = Get(param[0],param[1],param[2],param[3],"/v2/positions/FLEX")
Trades = Get(param[0],param[1],param[2],param[3],"/v2/positions/FLEX")
Orders = Get(param[0],param[1],param[2],param[3],"/v2/orders")
OrdersV21 = Get(param[0],param[1],param[2],param[3],"/v2.1/orders")
DeliveryOrders = Get(param[0],param[1],param[2],param[3],"/v2.1/delivery/orders")
Mint = Get(param[0],param[1],param[2],param[3],"/v2/mint/flexBTC")
Redeem = Get(param[0],param[1],param[2],param[3],"/v2/redeem/flexUSD")
Borrow = Get(param[0],param[1],param[2],param[3],"/v2/borrow/flexUSD")
Repay = Get(param[0],param[1],param[2],param[3],"/v2/repay/flexUSD")
BorrowingSummary = Get(param[0],param[1],param[2],param[3],"/v2/borrowingSummary")
FundingPayments = Get(param[0],param[1],param[2],param[3],"/v2/funding-payments")
Amm = Get(param[0],param[1],param[2],param[3],"/v2/AMM")

# Make requests here by commenting out the request you need
AccountInfo.makeRequest()
Balance.makeRequest()
BalanceId.makeRequest()
Postitions.makeRequest()
PostitionsId.makeRequest()
Trades.makeRequest()
Orders.makeRequest()
OrdersV21.makeRequest()
DeliveryOrders.makeRequest()
Mint.makeRequest()
Redeem.makeRequest()
Borrow.makeRequest()
Repay.makeRequest()
BorrowingSummary.makeRequest()
FundingPayments.makeRequest()
Amm.makeRequest()