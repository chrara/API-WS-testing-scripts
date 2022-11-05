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
        #'api.example.com', # API STAGE
        env, # API PROD
        key, # KEY
        secret, # SECRET
        123 # NONCE
)

simpleReq=0
ddos=0
sqlInject=1
wordlistPath="../../../Tools/Payloads/wordlist"
wordlistFile="/Injections/All_attack.txt"

class Get:
    def __init__(self,rest_url,api_key,api_secret,nonce,method):
        self.rest_url = rest_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.nonce = nonce
        self.method = method
    def makeRequest(self):
        ts = str(datetime.datetime.utcnow().isoformat())

        marketCodeIn=assetIn=subAccountIn=hashTokenIn=timeFrameIn=limitIn=startTimeIn=endTimeIn=""
        body = urlencode({"marketCode":marketCodeIn, "asset":assetIn, "hashToken":hashTokenIn, "subAcc": subAccountIn, "timeframe":timeFrameIn, "limit":limitIn, "startTime":startTimeIn,"endTime":endTimeIn})
        #body = urlencode({"hashToken":'CF-BTC-AMM-ZAcnrYy4', "asset": "BTC"})
        body=""

        msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, self.nonce, 'GET', self.rest_url, self.method, body)
        sig = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
        proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        header = {'Content-Type': 'application/json', 'AccessKey': self.api_key, 'User-Agent' : 'test7',
                'Timestamp': ts, 'Signature': sig, 'Nonce': str(self.nonce)}

        #############################################
        if(simpleReq==1):
                resp = requests.get("https://" + self.rest_url + self.method + '?'+ body, headers=header, proxies=proxies, verify=False )
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
                        def get_url(url):
                                return requests.get(url, headers=header, proxies=proxies, verify=False )
                        list_of_urls = [url]*1000
                        with ThreadPoolExecutor(max_workers=1000) as pool:
                                response_list = list(pool.map(get_url,list_of_urls))
                        for response in response_list:
                                x += 1
                                print(response.status_code, end=" ")
                                print(x)

        if(sqlInject==1):
                for r in wfuzz.fuzz(
                        url="https://" + self.rest_url + self.method + '?' + self.body, 
                        msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, self.nonce, 'GET', self.rest_url, self.method, self.body),
                        sig = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8'),
                        #printer=("path","raw"), 
                        headers=[
                        ('Connection', 'keep-alive'),
                        ('Content-Type', 'application/json'),
                        ('AccessKey', self.api_key),
                        ('User-Agent', 'test11'),
                        ('Timestamp', ts),
                        ('Signature', sig),
                        ('Nonce', str(self.nonce))],
                        method="GET",
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
##############################################
Account = Get(param[0],param[1],param[2],param[3],"/v3/account")#
Amm = Get(param[0],param[1],param[2],param[3],"/v3/AMM")#
AmmPositions = Get(param[0],param[1],param[2],param[3],"/v3/AMM/positions")#
AmmOrders = Get(param[0],param[1],param[2],param[3],"/v3/AMM/orders")#
AmmBalances = Get(param[0],param[1],param[2],param[3],"/v3/AMM/balances")#
AmmTrades = Get(param[0],param[1],param[2],param[3],"/v3/AMM/trades")#
AmmHash = Get(param[0],param[1],param[2],param[3],"/v3/AMM/hash-token")#
FlexAssetBalances = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/balances")#
NoteUSDBalances = Get(param[0],param[1],param[2],param[3],"/v3/noteusd/balances")
FlexAssetPositions = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/positions")#
FlexAssetYields = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/yields")#
NoteTokenYields= Get(param[0],param[1],param[2],param[3],"/v3/notetoken/yields")
Working= Get(param[0],param[1],param[2],param[3],"/v3/delivery/working")#
OrdersStatus = Get(param[0],param[1],param[2],param[3],"/v3/orders/status")#
Transfer = Get(param[0],param[1],param[2],param[3],"/v3/transfer")#
Balances = Get(param[0],param[1],param[2],param[3],"/v3/balances")# still in testing
Postitions = Get(param[0],param[1],param[2],param[3],"/v3/positions")# still in testing
Trades = Get(param[0],param[1],param[2],param[3],"/v3/trades")# still in testing
OrdersHistory = Get(param[0],param[1],param[2],param[3],"/v3/orders/history")# still in testing
WorkingOrders = Get(param[0],param[1],param[2],param[3],"/v3/orders/working")# still in testing
Delivery = Get(param[0],param[1],param[2],param[3],"/v3/delivery")# still in testing
Funding = Get(param[0],param[1],param[2],param[3],"/v3/funding")# still in testing
MintHistory = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/mint")#
RedeemHistory = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/redeem")#
EarnHistory = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/earned")#
NoteEarnHistory = Get(param[0],param[1],param[2],param[3],"/v3/notetoken/earned")
WithdrawHistory = Get(param[0],param[1],param[2],param[3],"/v3/withdrawal")
DepositAddress = Get(param[0],param[1],param[2],param[3],"/v3/deposit-addresses")#
DepositHistory = Get(param[0],param[1],param[2],param[3],"/v3/deposit")#
WithdrawAddresses = Get(param[0],param[1],param[2],param[3],"/v3/withdrawal-addresses")#
WithdrawFee = Get(param[0],param[1],param[2],param[3],"/v3/withdrawal-fee")#
Wallet = Get(param[0],param[1],param[2],param[3],"/v3/wallet")# still in testing
Orders = Get(param[0],param[1],param[2],param[3],"/v3/orders")# still in testing
AccountNames = Get(param[0],param[1],param[2],param[3],"/v3/account/names")# still in testing
# Comment out to run
#Working.makeRequest()
#Account.makeRequest()
#Amm.makeRequest() #unauthorized
#AmmPositions.makeRequest()
#AmmOrders.makeRequest()
#AmmBalances.makeRequest()
#AmmTrades.makeRequest()
#AmmHash.makeRequest()
#NoteTokenYields.makeRequest()
#OrdersStatus.makeRequest()
#Transfer.makeRequest()
Balances.makeRequest()
#Postitions.makeRequest()
#Trades.makeRequest()
#OrdersHistory.makeRequest()
#WorkingOrders.makeRequest()
#Delivery.makeRequest()
#Funding.makeRequest()
#MintHistory.makeRequest()
#RedeemHistory.makeRequest()
#EarnHistory.makeRequest()
#NoteEarnHistory.makeRequest()
#WithdrawHistory.makeRequest() #503
#DepositAddress.makeRequest() #503
#DepositHistory.makeRequest() #503
#WithdrawAddresses.makeRequest() #503
#WithdrawFee.makeRequest() #503
#Wallet.makeRequest()
#Orders.makeRequest()
#AccountNames.makeRequest()

#############################################################################################################
# docs.coinflex.com V3 PUBLIC
Tickers = Get(param[0],param[1],param[2],param[3],"/v3/tickers")#pub
Auction = Get(param[0],param[1],param[2],param[3],"/v3/auction")#pub
FundingRates = Get(param[0],param[1],param[2],param[3],"/v3/funding-rates")#pub
Candles = Get(param[0],param[1],param[2],param[3],"/v3/candles")#pub
Depth = Get(param[0],param[1],param[2],param[3],"/v3/depth")#pub
ExchangeTrades = Get(param[0],param[1],param[2],param[3],"/v3/exchange-trades")# still in testing
Markets = Get(param[0],param[1],param[2],param[3],"/v3/markets")#pub
Assets = Get(param[0],param[1],param[2],param[3],"/v3/assets")#pub
ExchangeRates = Get(param[0],param[1],param[2],param[3],"/v3/exchange-rates")#pub
FlexassetBalances = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/balances")#pub
NoteusdBalances = Get(param[0],param[1],param[2],param[3],"/v3/noteusd/balances")#pub
FlexassetPositions = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/positions")#pub
FlexassetOrders = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/orders")#pub
FlexassetTrades = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/trades")#pub
FlexassetDelivery = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/delivery")#pub
FlexassetYields = Get(param[0],param[1],param[2],param[3],"/v3/flexasset/yields")#pub
NotetokenYields = Get(param[0],param[1],param[2],param[3],"/v3/notetoken/yields")#pub
LeverageTiers= Get(param[0],param[1],param[2],param[3],"/v3/leverage-tiers")#pub
# Comment out to run
#Tickers.makeRequest()
#Auction.makeRequest()
#FundingRates.makeRequest()
#Candles.makeRequest()
#Depth.makeRequest()
#ExchangeTrades.makeRequest()
#Markets.makeRequest()
#Assets.makeRequest()
#ExchangeRates.makeRequest()
#FlexAssetBalances.makeRequest()
#NoteUSDBalances.makeRequest()
#FlexAssetPositions.makeRequest()
#FlexassetTrades.makeRequest()
#FlexassetOrders.makeRequest()
#FlexassetDelivery.makeRequest()
#FlexassetYields.makeRequest()
#NoteTokenYields.makeRequest()
#LeverageTiers.makeRequest()