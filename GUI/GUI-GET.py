import requests
import time
import logging
import config
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings("ignore")

xcf = config.xcf
csrf = config.csrf

endpoints= [
"v2/account/auth/trading/apiKeys/total"
,"v2/account/protected/account/permission"
,"v2/account/protected/accounts/antiphish/get"
,"v2/account/protected/accounts/normal/list"
,"v2/account/protected/accounts/whitelist/switch/email"
,"v2/account/protected/balance/info/28610"
,"v2/account/protected/balances?needDisplay=false&accountId=28610"
,"v2/account/protected/current/login"
,"v2/account/protected/dashboard"
,"v2/account/protected/deposit/balance/BCH"
,"v2/account/protected/deposit/coin/LINEAR"
,"v2/account/protected/deposit/coin/Liner"
,"v2/account/protected/estimated/balance/28610"
,"v2/account/protected/estimated/balance/28610"
,"v2/account/protected/favorite/markets"
,"v2/account/protected/geetest/CREATE_SUB_ACCOUNT"
,"v2/account/protected/kyc/information"
,"v2/account/protected/max/withdraw/amount/USD"
,"v2/account/protected/spot/types"
,"v2/account/protected/tfa/reminds?action=TFA_BALANCE_REMIND"
,"v2/account/protected/tfa/reminds?action=TFA_DEPOSIT_REMIND"
,"v2/account/protected/tfa/reminds?action=TFA_DEPOSIT_REMIND"
,"v2/account/protected/tfa/reminds?action=TFA_REGISTER_REMIND"
,"v2/account/protected/tfa/types"
,"v2/account/protected/trading/account/level"
,"v2/account/protected/trading/switch/account"
,"v2/account/protected/transfers/internal/accounts/combos"
,"v2/account/protected/true/white/list"
,"v2/account/protected/ui-settings"
,"v2/account/protected/withdraw/addresses"
,"v2/account/protected/withdraw/balance/USD"
,"v2/account/protected/withdraw/fee/USD"
,"v2/account/protected/withdraw/limit"
,"v2/account/public/default/favorites"
,"v2/account/tfa/login"
]

header = {
    'Content-Type': 'application/json', 
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Host' : 'api.example.com',
    'Accept' : 'application/json, text/plain, */*',
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip, deflate',
    'Content-Type' : 'application/json;charset=utf-8',
    'X-Cf-Token' : xcf,
    'Cookie' : csrf,
    'Origin' : 'https://v2stg.coinflex.com',
    'Dnt' : '1',
    'Referer' : 'https://v2stg.coinflex.com/',
    'Sec-Fetch-Dest' : 'empty',
    'Sec-Fetch-Mode' : 'cors',
    'Sec-Fetch-Site' : 'same-site',
    'Te' : 'trailers'
}

host="https://api.example.com/"
endpoint="v2/account/auth/trading/apiKeys/total"
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

burp=1
multi=1
ddos=0
sing=0

if(ddos==1):
    i = 1
    x = 0
    while i <= 50:
      i += 1
      def get_url(url):
          return requests.get(url, headers=header, proxies=proxies, verify=False )
      list_of_urls = [host + endpoint]*10000
      with ThreadPoolExecutor(max_workers=100) as pool:
          response_list = list(pool.map(get_url,list_of_urls))
      for response in response_list:
          x += 1
          print(response.status_code, end=" ")
          print(x)

if(sing==1):
    if(burp==1):
        response = requests.get(str(host) + "v2/account/auth/trading/apiKeys/total",headers=header, proxies=proxies, verify=False)
    else:
        response = requests.get(str(host) + "v2/account/auth/trading/apiKeys/total",headers=header)
        print(str(response.status_code) + " " + str(response.reason))
        print(str(response.content) + "\n")

if(multi==1):
    for x in endpoints:
        if(burp==1):
            response = requests.get(str(host) + x.rstrip("\n"),headers=header, proxies=proxies, verify=False)
        else:
            response = requests.get(str(host) + x.rstrip("\n"),headers=header)
            print(str(response.status_code) + " " + str(response.reason) + " " + x)
            print(str(response.content) + "\n")