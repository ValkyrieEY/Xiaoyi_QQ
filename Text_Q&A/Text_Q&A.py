import json
import os

__name__ = "Text_Parser"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

QA_FILE = "qa_data.json"

def load_qa_data():
    if os.path.exists(QA_FILE):
        with open(QA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_qa_data(data):
    with open(QA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

qa_data = load_qa_data()

async def on_message(event, actions):
    message = str(event.message).strip()
    
    if message.startswith("学习 "):
        parts = message[3:].split(" ", 1)
        if len(parts) == 2:
            question, answer = parts
            qa_data[question] = answer
            save_qa_data(qa_data)
            return f"我学会了! 问题: {question}, 答案: {answer}"
        else:
            return "格式错误,请使用'学习 问题 答案'的格式"
    
    elif message.startswith("忘记 "):
        question = message[3:].strip()
        if question in qa_data:
            del qa_data[question]
            save_qa_data(qa_data)
            return f"我已经忘记了关于'{question}'的回答"
        else:
            return f"我没有学过关于'{question}'的回答"
    
    elif message in qa_data:
        return qa_data[message]
    
    return None  # 如果没有匹配的问题,返回None,让主程序继续处理
