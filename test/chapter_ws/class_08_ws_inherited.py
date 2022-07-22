
"""
    Bitmex Websocket

    1. 先登录websocket, 然后订阅数据...

"""

import json
import sys
import traceback
import socket
from datetime import datetime
from time import sleep
from threading import Lock, Thread
import websocket
import zlib
import time
import hashlib
import hmac
import base64

from chapter_ws.base_websocket import Tick, BaseWebsocket


class BitmexWebsocket(BaseWebsocket):
    """
        Websocket API
        创建Websocket client对象后，需要调用Start的方法去启动workder和ping线程
        1. Worker线程会自动重连.
        2. 使用stop方法去停止断开和销毁websocket client,
        3. 四个回调方法..
        * on_open
        * on_close
        * on_msg
        * on_error

        start()方法调用后，ping线程每隔60秒回自动调用一次。

    """
    def __init__(self):
        super(BitmexWebsocket, self).__init__(host="wss://www.bitmex.com/realtime", ping_interval=20)
        self.bids = {}
        self.asks = {}
        self.ticks = {}

    def on_open(self):
        """on open """
        print("on open")
        self.authenticate()

        self.send_msg({"op": "subscribe", "args": ["orderBookL2_25:XBTUSD", "orderBookL2_25:ETHUSD"]})

    def authenticate(self):
        key = "YXh065IjxaxWuBXAsDJr8u6g"  # id
        secret = "x_FUiNfq-kXz2Ml5MoyaUDBINsFDwJC3A2qhswvulCcDO-Tv"
        expires = int(time.time())
        method = "GET"
        path = "/realtime"
        msg = method + path + str(expires)
        signature = hmac.new(secret.encode("utf-8"), msg.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()
        data = {"op": "authKey", "args": [key, expires, signature]}
        self.send_msg(data)
    def on_close(self):
        """
        on close websocket
        """

    def on_msg(self, data: str):

        """call when the msg arrive."""
        msg = json.loads(data)
        # print(msg)

        #如果登录成功，就定义账户相关的信息..
        if "request" in msg:
            req = msg["request"]
            success = msg["success"]
            if success:
                if req["op"] == 'authKey':
                    self.subscribe_private_data()

        elif "table" in msg:
            if msg["table"] == "orderBookL2_25":
                symbol = None
                if msg['action'] == 'partial':
                    data = msg['data']
                    for item in data:
                        symbol = item['symbol']
                        ask = self.asks.setdefault(symbol, {})
                        bid = self.bids.setdefault(symbol, {})
                        id_ = item['id'] # id
                        side = item['side']
                        if side == 'Buy':
                            bid[id_] = item
                        else:
                            ask[id_] = item

                elif msg['action'] == 'update':
                    data = msg['data']
                    for item in data:
                        symbol = item['symbol']
                        id_ = item['id']
                        side = item['side']
                        ask = self.asks.setdefault(symbol, {})
                        bid = self.bids.setdefault(symbol, {})
                        if side == 'Buy' and bid.get(id_):
                            bid[id_].update(item)
                        elif side == 'Sell' and ask.get(id_):
                            ask[id_].update(item)

                elif msg['action'] == 'delete':
                    data = msg['data']
                    for item in data:
                        symbol = item['symbol']
                        id_ = item['id']
                        side = item['side']
                        ask = self.asks.setdefault(symbol, {})
                        bid = self.bids.setdefault(symbol, {})

                        if side == 'Buy':
                            if bid.get(id_):
                                del bid[id_]
                        else:
                            if ask.get(id_):
                                del ask[id_]

                elif msg['action'] == 'insert':
                    data = msg['data']
                    for item in data:
                        symbol = item['symbol']
                        id_ = item['id']
                        side = item['side']

                        ask = self.asks.setdefault(symbol, {})
                        bid = self.bids.setdefault(symbol, {})
                        if side == 'Buy':
                            bid[id_] = item
                        else:
                            ask[id_] = item

                if symbol:
                    ask_list = list(self.asks.get(symbol).items())
                    bid_list = list(self.bids.get(symbol).items())
                    self.on_orderbook(symbol=symbol, ask_list=ask_list, bid_list=bid_list)

    def on_orderbook(self, symbol, ask_list, bid_list):
        tick = self.ticks.get(symbol, None)
        print(tick)
        if not tick:
            tick = Tick()
            self.ticks[symbol] = tick

        ask_list.sort(key=lambda x: x[1]['price'], reverse=False)
        bid_list.sort(key=lambda x: x[1]['price'], reverse=True)
        # print(ask_list)
        # print("*"* 10)
        # print(bid_list)
        bid_length = len(bid_list) if len(bid_list) < 5 else 5
        ask_length = len(ask_list) if len(ask_list) < 5 else 5

        for n in range(bid_length):
            data = bid_list[n][1]
            tick.__setattr__("bid_price_" + str(n + 1), float(data['price']))
            tick.__setattr__("bid_volume_" + str(n + 1), float(data['size']))

        for n in range(ask_length):
            data = ask_list[n][1]
            tick.__setattr__("ask_price_" + str(n + 1), float(data['price']))
            tick.__setattr__("ask_volume_" + str(n + 1), float(data['size']))

        print(tick.ask_price_5, tick.ask_volume_5)
        print(tick.ask_price_4, tick.ask_volume_4)
        print(tick.ask_price_3, tick.ask_volume_3)
        print(tick.ask_price_2, tick.ask_volume_2)
        print(tick.ask_price_1, tick.ask_volume_1)
        print("*"* 20)
        print(tick.bid_price_1, tick.bid_volume_1)
        print(tick.bid_price_2, tick.bid_volume_2)
        print(tick.bid_price_3, tick.bid_volume_3)
        print(tick.bid_price_4, tick.bid_volume_4)
        print(tick.bid_price_5, tick.bid_volume_5)

    def subscribe_private_data(self):
        data = {"op": "subscribe", "args":["execution:XBTUSD", "order:XBTUSD", "margin", "position:XBTUSD"]}
        self.send_msg(data)


if __name__ == '__main__':
    okex_ws = BitmexWebsocket()
    okex_ws.start()

