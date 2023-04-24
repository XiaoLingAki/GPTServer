import websocket


def chatgpt_request(text):

    list1 = []
    def on_message(ws, message):
        # print('接收信息：' + message)
        list1.append(message)

    def on_error(ws, error):
        print('API调用发生错误，请检查网络情况')
        print(error)

    def on_close(ws, message, error):
        # print('WebSocket object:')
        # print(ws)
        print('Connection closed.')

    def on_open(ws):
        sentence = text
        ws.send(sentence)
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("ws://8.222.159.238:8888",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()

    # print(list1[0])
    return list1[0]


if __name__ == '__main__':
    text = '''
    请帮我写一篇语言生成模型的训练计划书，内容包括开发的具体方案和流程，主要有以下两种训练方案。
    1.训练方案1：采用ChatGLM-chinese-instruct训练。这种方法是基于lora技术的。
    2.训练方案2：采用ChatGLM-Ptuning进行训练。
    计划书应论述以上两种训练方法的利弊，尽量多于1000字。
    '''
    print(chatgpt_request(text))

