import config
import websockets
import asyncio
import json
import time

#xcf token stored in external file for security
xcf = config.xcf # replace with x-cf token from localstorage

url = "wss://v2api.bitcoin.com"
ts = str(int(time.time() * 1000))
guiauth={"op":"login","data":{"loginId":"99999999","xCFToken":xcf}}
endpoint="/v2/websocket"
url=url+endpoint

place_order = \
{
"op": "placeorder",
"tag": 123,
"data": {
            "timestamp": ts,
            "recvWindow": 2000,
            "clientOrderId": 1,
            "marketCode": "ETHd-USD",
            "side": "SELL",
            "orderType": "LIMIT",
            "quantity": 0.001,
            "timeInForce": "GTC",
            "price": 44567
        }
}

header = {
    'Content-Type': 'application/json', 
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Host' : 'api.example.com',
    'Accept' : 'application/json, text/plain, */*',
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip, deflate',
    'Content-Type' : 'application/json;charset=utf-8',
    'X-Cf-Token' : xcf,
    'Cookie' : "csrftoken=",
    'Origin' : 'https://exchange.bitcoin.com',
    'Dnt' : '1',
    'Referer' : 'https://exchange.bitcoin.com',
    'Sec-Fetch-Dest' : 'empty',
    'Sec-Fetch-Mode' : 'cors',
    'Sec-Fetch-Site' : 'same-site',
    'Connection' : 'upgrade',
    'Pragma': 'no-cache',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    'Sec-WebSocket-Key' : 'JQdCp4o1S+TVYpydcLS1QA==',
    'Sec-WebSocket-Version' : '13',
    'Te' : 'trailers'
}

async def subscribe():
    async with websockets.connect(url,extra_headers=header) as ws:
        while True:
            if not ws.open:
                print("websocket disconnected")
                ws = await websockets.connect(url)
            response = await ws.recv()
            data = json.loads(response)
            print(data)
            if 'nonce' in data:
                    await ws.send(json.dumps(guiauth))
            elif 'event' in data and data['event'] == 'login':
                if data['success'] == True:
                    await ws.send(json.dumps(place_order))
            elif 'event' in data and data['event'] == 'placeorder':
                continue
asyncio.get_event_loop().run_until_complete(subscribe()) 