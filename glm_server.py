import os
import platform
import signal
from transformers import AutoTokenizer, AutoModel
import websockets
import asyncio

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
model = model.eval()

os_name = platform.system()
clear_command = 'cls' if os_name == 'Windows' else 'clear'
stop_stream = False


def build_prompt(history):
    prompt = "欢迎使用 ChatGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序"
    for query, response in history:
        prompt += f"\n\n用户：{query}"
        prompt += f"\n\nChatGLM-6B：{response}"
    return prompt


def signal_handler(signal, frame):
    global stop_stream
    stop_stream = True


# def main():
#     history = []
#     global stop_stream
#     print("欢迎使用 ChatGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
#     while True:
#         query = input("\n用户：")
#         if query == "stop":
#             break
#         if query == "clear":
#             history = []
#             os.system(clear_command)
#             print("欢迎使用 ChatGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
#             continue
#         count = 0
#         for response, history in model.stream_chat(tokenizer, query, history=history):
#             if stop_stream:
#                 stop_stream = False
#                 break
#             else:
#                 count += 1
#                 if count % 8 == 0:
#                     os.system(clear_command)
#                     print(build_prompt(history), flush=True)
#                     signal.signal(signal.SIGINT, signal_handler)
#         os.system(clear_command)
#         print(build_prompt(history), flush=True)


class Character:
    def __init__(self, name, age, kind):
        self.name = name
        self.age = age
        self.kind = kind


def prompt_select(chara=Character('小琪', '17', '少女')):
    prompt = '''假设你是一个名字叫做''' + chara.name + '''的''' + chara.kind + '''，你的年龄是''' + chara.age + '''岁，请你以这个身份应有的语气和说话方式进行对话。\n'''
    # prompt += '''你只需要回答“我的问题是：”这几个字后面的问题。'''
    print(prompt)
    return prompt


memory = '聊天记录：\n'  # 存储聊天记录
def generate(text, prompt=''):
    global stop_stream
    global history
    global memory
    query = prompt + text
    print(query)
    count = 0
    for response, history in model.stream_chat(tokenizer, query):
        pass
        # print(response)
        # print(history)
    memory += '用户：' + text + '\n' + '回答：' + history[0][1] + '\n'
    re = history[0][1]
    print(re)
    return re


async def socket_glm(websocket, path):
    input_text = await websocket.recv()
    answer = generate(input_text, prompt_select())
    await websocket.send(answer)


def run_glm():
    start_server = websockets.serve(socket_glm, "192.168.0.149", 8888, ping_interval=None)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    # generate()
    run_glm()

