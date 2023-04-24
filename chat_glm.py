import os
import platform
import signal
import gradio as gr

from transformers import AutoTokenizer, AutoModel

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
    prompt = '''假设你是一个名字叫做''' + chara.name + '''的''' + chara.kind + '''，你的年龄是''' + chara.age + '''岁，请你以这个身份应有的语气和说话方式回答我的问题。\n'''
    prompt += ''''''
    print(prompt)
    return prompt


def chat_once(text, history=None):
    if history is None:
        history = []

    print(history)
    query = text
    # query = input("\n用户：")
    response, history = model.chat(tokenizer, query, history=history)
    print(response)
    return history


h = []
def chat(text):
    global h
    if len(h) < 1:
        h = chat_once(prompt_select() + text)
    else:
        print(h)
        h = chat_once(text, history=h)
        print(h)
        print(h[-1][1])


def main():
    history = []
    global stop_stream
    print("欢迎使用 ChatGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
    while True:
        query = input("\n用户：")
        if query == "stop":
            break
        if query == "clear":
            history = []
            os.system(clear_command)
            print("欢迎使用 ChatGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
            continue
        count = 0
        for response, history in model.stream_chat(tokenizer, query, history=history):
            if stop_stream:
                stop_stream = False
                break
            else:
                count += 1
                if count % 8 == 0:
                    os.system(clear_command)
                    print(build_prompt(history), flush=True)
                    signal.signal(signal.SIGINT, signal_handler)
        os.system(clear_command)
        print(build_prompt(history), flush=True)


if __name__ == "__main__":
    # chat(prompt_select())
    while True:
        chat(input('请输入：'))
    # main()
