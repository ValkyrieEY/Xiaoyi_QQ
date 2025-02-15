import json
import os
from Hyper import Manager, Segments

# 插件元数据
TRIGGHT_KEYWORD = "Any"  # 需要处理所有消息来匹配问答
HELP_MESSAGE = """问答学习系统
指令：
学习 <问题> <答案> - 教机器人记住一个问答
忘记 <问题> - 删除一个已学习的问答"""

__name__ = "Text_Parser"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

# 配置文件路径
QA_FILE = os.path.join(os.path.dirname(__file__), "qa_data.json")

def load_qa_data():
    if os.path.exists(QA_FILE):
        try:
            with open(QA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Text_Parser] 加载问答数据失败: {str(e)}")
            return {}
    return {}

def save_qa_data(data):
    try:
        with open(QA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[Text_Parser] 保存问答数据失败: {str(e)}")
        return False

qa_data = load_qa_data()

async def on_message(event, actions, Manager, Segments):
    message = str(event.message).strip()
    
    if message.startswith("学习 "):
        parts = message[3:].split(" ", 1)
        if len(parts) == 2:
            question, answer = parts
            qa_data[question] = answer
            if save_qa_data(qa_data):
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text(f"我学会了！\n问题：{question}\n答案：{answer}"))
                )
            else:
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text("保存问答数据失败"))
                )
            return True
        else:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("格式错误，请使用'学习 问题 答案'的格式"))
            )
            return True
    
    elif message.startswith("忘记 "):
        question = message[3:].strip()
        if question in qa_data:
            del qa_data[question]
            if save_qa_data(qa_data):
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text(f"我已经忘记了关于'{question}'的回答"))
                )
            else:
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text("保存更改失败"))
                )
            return True
        else:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"我没有学过关于'{question}'的回答"))
            )
            return True
    
    elif message in qa_data:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(qa_data[message]))
        )
        return True
    
    return False
