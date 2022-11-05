import requests
import config
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings("ignore")

xcf = config.xcf
csrf = config.csrf

url=[
"https://api.example.com/v2/lending/protected/earns/zrt/submit"
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

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
body = '{"productId": "774437561750781957","action": "ZRT","quantity": "10000"}'


for x in url:
    response = requests.post(x.rstrip("\n"),headers=header, data=body, proxies=proxies, verify=False)
    print(str(response.status_code) + " " + str(response.reason) + " " + x)
    print(str(response.content) +"\n")

