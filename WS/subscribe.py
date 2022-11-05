import time
import config
import websockets
import asyncio
import json
import hmac
import base64
import hashlib

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
            "recvWindow": 2000,
            "clientOrderId": 1,
            "marketCode": "BTC-USD",
            "side": "SELL",
            "orderType": "LIMIT",
            "quantity": 0.001,
            "timeInForce": "GTC",
            "price": 44000
        }
}

url = host + endpoint
async def subscribe():
    async with websockets.connect(url) as ws:
        while True:
            if not ws.open:
                print("websocket disconnected")
                ws = await websockets.connect(url)
            response = await ws.recv()
            data = json.loads(response)
            print(data)
            if 'nonce' in data:
                    await ws.send(json.dumps(auth))
            elif 'event' in data and data['event'] == 'login':
                if data['success'] == True:
                    await ws.send(json.dumps(balance))
                    #await ws.send(json.dumps(position))
                    #await ws.send(json.dumps(order))
                    #await ws.send(json.dumps(subAll))
                    """""
                    Check balance
                    If balance is > 5
                    await ws.send(json.dumps(place_order))
                    """
            elif 'table' in data and data['table'] == 'balance':
                 if(float(data["data"][0]["available"]) > 2.0):
                  await ws.send(json.dumps(place_order))
                 continue
            elif 'event' in data and data['event'] == 'position':
                 continue
            elif 'event' in data and data['event'] == 'order':
                 continue
            
asyncio.get_event_loop().run_until_complete(subscribe()) 