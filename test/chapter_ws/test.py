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

asks = {}
bids = {}

def on_open(ws):
    print("on open")

    data = {"op": "subscribe", "args": ["orderBookL2_25:XBTUSD"]}
    ws.send(json.dumps(data))


def on_message(ws, msg):

    msg = json.loads(msg)
    # print(msg)

    if "table" in msg:
       if msg["table"] == "orderBookL2_25":

            data = msg["data"]

            if msg['action'] == 'partial':
                for item in data:
                    if item['side'] == 'Sell':
                        asks[item['id']] = item
                    else:
                        bids[item['id']] = item

            elif msg['action'] == 'update':
                for item in data:
                    if item['side'] == 'Sell':
                        asks[item['id']].update(item)

                    else:
                        bids[item['id']].update(item)

            elif msg['action'] == 'delete':
                for item in data:
                    if item['side'] == 'Sell':
                        if item['id'] in asks:
                            del asks[item['id']]

                    else:
                        if item['id'] in bids:
                            del bids[item['id']]

            elif msg['action'] == 'insert':
                for item in data:
                    if item['side'] == 'Sell':
                        asks[item['id']] = item
                    else:
                        bids[item['id']] = item

            asks_list = list(asks.items())
            bids_list = list(bids.items())

            print(asks_list)

            print("ask_length=>", str(len(asks_list)))
            print("bid_length=>", str(len(bids_list)))

            asks_list.sort(key=lambda x: x[1]['price'], reverse=False)
            bids_list.sort(key=lambda x: x[1]['price'], reverse=True)

            # print(asks_list)
            # print("*" * 10)
            # print(bids_list)
            # print("\n" * 5)

            # asks_list = asks_list[0:6]
            # bids_list = bids_list[0:6]

            for n in range(5):
                data = bids_list[n][1]
                tick.__setattr__("bid_price_" + str(n+1), float(data['price']))
                tick.__setattr__("bid_volume_" + str(n+1), float(data['size']))

            for n in range(5):
                data = asks_list[n][1]
                tick.__setattr__("ask_price_" + str(n + 1), float(data['price']))
                tick.__setattr__("ask_volume_" + str(n + 1), float(data['size']))

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
    ws_url = "wss://www.bitmex.com/realtime"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close
                                )
    ws.run_forever(ping_interval=15)



