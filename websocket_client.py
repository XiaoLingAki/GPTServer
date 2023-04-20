# -*-encoding:"utf-8"-*-
import time
import datetime
import websocket



def on_message(ws, message):
    print('接收信息：' + message)


def on_error(ws, error):
    print('出现错误')
    print(error)


def on_close(ws, message, error):
    print('WebSocket object:')
    print(ws)
    print('Connection closed.')


def on_open(ws):
    sentence = input("请输入:")
    ws.send(sentence)


while True:
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("ws://192.168.0.149:8888",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()
