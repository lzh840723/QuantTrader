import websocket
import json
import zlib


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

    data = {"sub": "market.btcusdt.depth.step1", "id": 1}
    ws.send(json.dumps(data))


def on_message(ws, msg):

    msg = json.loads(zlib.decompress(msg, 31))
    # # print(msg)


    if "ping" in msg:
        ws.send(json.dumps({"pong": msg["ping"]}))

    if 'ch' in msg:
        channel = msg.get('ch')
        if "depth.step1" in channel:
            bids = msg['tick']['bids']
            asks = msg['tick']['asks']

            for n in range(5):
                price, volume = bids[n]
                tick.__setattr__("bid_price_" + str(n+1), float(price))
                tick.__setattr__("bid_volume_" + str(n+1), float(volume))

            for n in range(5):
                price, volume = asks[n]
                tick.__setattr__("ask_price_" + str(n + 1), float(price))
                tick.__setattr__("ask_volume_" + str(n + 1), float(volume))

            print(tick.ask_price_5, tick.ask_volume_5)
            print(tick.ask_price_4, tick.ask_volume_4)
            print(tick.ask_price_3, tick.ask_volume_3)
            print(tick.ask_price_2, tick.ask_volume_2)
            print(tick.ask_price_1, tick.ask_volume_1)
            print("*" * 30)
            print(tick.bid_price_1, tick.bid_volume_1)
            print(tick.bid_price_2, tick.bid_volume_2)
            print(tick.bid_price_3, tick.bid_volume_3)
            print(tick.bid_price_4, tick.bid_volume_4)
            print(tick.bid_price_5, tick.bid_volume_5)

            print("\n" * 5)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print()




if __name__ == '__main__':
    ws_url = "wss://api.huobi.vn/ws"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close
                                )
    ws.run_forever(ping_interval=15)


