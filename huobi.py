# huobi现货 websocket
import websocket
import json
import zlib
import time


def on_open(ws):
    print("on open")
    #订阅
    data = { "sub": "market.btcusdt.depth.step0", "id": "id1" }
    ws.send(json.dumps(data))


def on_message(ws, msg):
    print("on message")
    t1 = time.time_ns()
    #解压数据
    msg = json.loads(zlib.decompress(msg, 31))
    t2 = time.time_ns()
    print(msg)

    print(t2 - t1)
    #回传ping pong
    if "ping" in msg:
        ws.send(json.dumps({"pong": msg['ping']}))



def on_error(ws, error):
    print("on error")
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("on close")


if __name__ == '__main__':
    ws_url = "wss://api.huobi.pro/ws"

    ws = websocket.WebSocketApp(ws_url, on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever(ping_interval=15)
