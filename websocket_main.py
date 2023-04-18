import asyncio
import websockets
from chat_gpt import *

history = '聊天记录：'
# async def socket_gpt(websocket, path):
#     global history
#     if len(history) > 1600:
#         history = '聊天记录：' + history[800:]
#     input_text = await websocket.recv()
#     history += input_text + '  '
#     print(f"{input_text}")
#
#     answer = digital_person_chat(prompt_select(), history, input_text)
#     print(answer)
#     history += answer + '  '
#
#     await websocket.send(answer)

async def socket_gpt(websocket, path):
    input_text = await websocket.recv()
    answer = chatgpt(input_text)
    await websocket.send(answer)


def run_gpt():
    start_server = websockets.serve(socket_gpt, "192.168.0.149", 8888, ping_interval=None)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    run_gpt()
