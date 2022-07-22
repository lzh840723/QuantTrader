"""
1. 简单连接weboscket..
2. okex简单的使用..
"""


import websocket
import json
import zlib

# from dataclasses import dataclass
# @dataclass

class Tick(object):
    def __init__(self):
        self.bid_price_1 = 0
        self.bid_price_2 = 0
        self.bid_price_3 = 0
        self.bid_price_4 = 0
        self.bid_price_5 = 0

        self.ask_price_1 = 0
        self.ask_price_2 = 0
        self.ask_price_3 = 0
        self.ask_price_4 = 0
        self.ask_price_5 = 0

        self.bid_volume_1 = 0
        self.bid_volume_2 = 0
        self.bid_volume_3 = 0
        self.bid_volume_4 = 0
        self.bid_volume_5 = 0

        self.ask_volume_1 = 0
        self.ask_volume_2 = 0
        self.ask_volume_3 = 0
        self.ask_volume_4 = 0
        self.ask_volume_5 = 0


tick = Tick()

def on_open(ws):
    print("on open")
    data = {"op": "subscribe", "args": ["swap/depth5:BTC-USD-SWAP"]}
    ws.send(json.dumps(data))

def on_close(ws):
    print("On close")

def on_error(ws, error):
    print(f"on error: {error}")

def on_message(ws, msg):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )

    msg = json.loads(decompress.decompress(msg))
    # print(msg)
    if 'table' in msg and msg['table'] == 'swap/depth5':
        data = msg['data']
        for item in data:
            bids = item["bids"]
            asks = item["asks"]

            for n, buf in enumerate(bids):
                price, volume, _, __ = buf
                tick.__setattr__("bid_price_%s" % (n + 1), price)
                tick.__setattr__("bid_volume_%s" % (n + 1), volume)

            for n, buf in enumerate(asks):
                price, volume, _, __ = buf
                tick.__setattr__("ask_price_%s" % (n + 1), price)
                tick.__setattr__("ask_volume_%s" % (n + 1), volume)

            print(tick.ask_price_5, tick.ask_volume_5)
            print(tick.ask_price_4, tick.ask_volume_4)
            print(tick.ask_price_3, tick.ask_volume_3)
            print(tick.ask_price_2, tick.ask_volume_2)
            print(tick.ask_price_1, tick.ask_volume_1)
            print("*"*30)
            print(tick.bid_price_1, tick.bid_volume_1)
            print(tick.bid_price_2, tick.bid_volume_2)
            print(tick.bid_price_3, tick.bid_volume_3)
            print(tick.bid_price_4, tick.bid_volume_4)
            print(tick.bid_price_5, tick.bid_volume_5)

            print("\n"*5)




if __name__ == '__main__':

    wss_url = "wss://real.okex.com:8443/ws/v3"
    ws = websocket.WebSocketApp(wss_url,
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error
                                )

    ws.run_forever(ping_interval=15)


