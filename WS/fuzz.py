import time
import config
import websockets
import asyncio
import json
import hmac
import base64
import hashlib
import time

api_key = config.key
api_secret = config.secret
ts = str(int(time.time() * 1000))
sig_payload = (ts+'GET/auth/self/verify').encode('utf-8')
signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), sig_payload, hashlib.sha256).digest()).decode('utf-8')

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
host="wss://api.example.com"
endpoint="/v1/websocket"

auth = \
{
"op": "login",
"tag": 1,
"data": {
        "apiKey": api_key,
        "timestamp": ts,
        "signature": signature
        }
}

balance = \
{
  "op": "subscribe",
  "args": ["balance:all"],
  "tag": 101
}

position = \
{
  "op": "subscribe", 
  "args": ["position:all"], 
  "tag": 102
}

order = \
{
  "op": "subscribe", 
  "args": ["order:all"], 
  "tag": 102
}

subAll = \
{
  "op": "subscribe", 
  "args": ["order:all","balance:all","position:all"], 
  "tag": 102
}

place_order = \
{
"op": "placeorder",
"tag": 123,
"data": {
            "timestamp": ts,
            "recvWindow": 100000000,
            "clientOrderId": 1,
            "marketCode": "BTC-USD",
            "side": "SELL",
            "orderType": "LIMIT",
            "quantity": 0.001,
            "timeInForce": "GTC",
            "price": 46600
        }
}

#{'event': 'placeorder', 'submitted': False, 'tag': '123', 'message': 'marketCode is invalid', 'code': '20015', 'timestamp': '1648894458343', 'data': {'recvWindow': 2000, 'timestamp': 1648894455408, 'clientOrderId': '1', 'marketCode': 'btcUSD', 'side': 'SELL', 'orderType': 'LIMIT', 'quantity': '0.001', 'timeInForce': 'GTC', 'price': '44000', 'source': 0}}
#{'table': 'balance', 'accountId': '100130', 'timestamp': '1648896085843', 'tradeType': 'LINEAR', 'data': [{'total': '2.998', 'reserved': '0.000', 'instrumentId': 'BTC', 'available': '2.998', 'quantityLastUpdated': '1648621136173'}, {'total': '1', 'reserved': '0.00', 'instrumentId': 'ETH', 'available': '1.00', 'quantityLastUpdated': '1648621073520'}, {'total': '1', 'reserved': '0', 'instrumentId': 'BCH', 'available': '1', 'quantityLastUpdated': '1648049738190'}, {'total': '13.674436000', 'reserved': '0.0000', 'instrumentId': 'flexUSD', 'available': '13.674436000', 'quantityLastUpdated': '1648882862996'}]}

#################################################################################### FUZZ CONFIG
wordlistPath="../../../Tools/Payloads/wordlist/"
fuzzWords = open(wordlistPath+'general/test.txt', 'r')
Lines = fuzzWords.readlines()
place_order_data_field = "marketCode"
#################################################################################### FUZZ CONFIG END
url = host + endpoint
async def subscribe():
    async with websockets.connect(url) as ws:
        while True:
            if not ws.open:
                print("websocket disconnected")
                ws = await websockets.connect(url)
            response = await ws.recv()
            data = json.loads(response)
            #print(data)
            if 'event' in data and data['event'] == 'placeorder':
              print(data)
              time.sleep(0.15)
            if 'nonce' in data:
                    await ws.send(json.dumps(auth))
            elif 'event' in data and data['event'] == 'login':
                if data['success'] == True:
#################################################################################### SUBSCRIBE START
                    await ws.send(json.dumps(balance))
                    #await ws.send(json.dumps(position))
                    #await ws.send(json.dumps(order))
                    #await ws.send(json.dumps(subAll))
#################################################################################### SUBSCRIBE END
            elif 'table' in data and data['table'] == 'balance':
#################################################################################### TRADE IF BALANCE CHECK START
                  if(float(data["data"][0]["available"]) > 2.2): # BTC
#################################################################################### FUZZ START
                    count = 0
                    for line in Lines:
                        count += 1
                        place_order["data"][place_order_data_field] = line.rstrip("\n")
                        await ws.send(json.dumps(place_order))
#################################################################################### FUZZ END
#################################################################################### TRADE IF BALANCE CHECK END
            elif 'event' in data and data['event'] == 'position':
                 continue
            elif 'event' in data and data['event'] == 'order':
                 continue
            
asyncio.get_event_loop().run_until_complete(subscribe()) 