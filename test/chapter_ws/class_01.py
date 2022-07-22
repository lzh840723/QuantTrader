"""
## 什么是websocket?

1.1WebSocket 协议在2008年诞生，2011年成为国际标准。WebSocket API是HTML5标准的一部分，
但这并不代表 WebSocket 一定要用在 HTML 中，或者只能在基于浏览器的应用程序中使用。主流的编程语言都支持websocket现在

1.2 python的websocket库有 websocket-client, websockets, aiowebsocket

1.3 目前的主流交易所都支持Websocket通信
1.4 WebSocket 的最大特点就是，服务器可以主动向客户端推送信息，客户端也可以主动向服务器发送信息，是真正的双向平等对话。


## http和websocket的区别
http 类似发送短信的功能
websocket 有点类似于电话的功能

websocket相比http通讯更加高效，传递的信息更少，不需要传递那么多的headers信息，节省带宽等

2. http/https ws/wss
https://主机:端口号/路径

wss://real.okex.com:10834/ws

3. 为什么要用websocket呢？
1. http请求过多容易造成服务器限制，或者攻击服务器DDOS攻击服务器 ticker // orderbook // 0.5
2. 数据的时效性

websocket 一般会告诉我们一下四种状态：

on_open  连接成功
on_message 新的消息
on_error 发生错误
on_close 连接关闭

send()

服务器为了保持跟客户端连接，客户端需要跟客户端进行ping和pong的交互，发送心跳包，让服务器知道客户端还处于在线的状态
1. 客户端需要定时的发送ping命令到服务器
2. 服务器发送ping的消息后，客户端收到后，需要回复pong的消息.

websocket可以通过发送数据给服务器。


"""