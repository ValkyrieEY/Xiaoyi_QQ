import json
import os
from Hyper import Manager, Segments

# 添加文件路径常量
MANAGE_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Manage_User.ini")
SUPER_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Super_User.ini")

# 修改插件元数据和帮助信息
TRIGGHT_KEYWORD = "Any"
HELP_MESSAGE = """问答学习系统
普通用户指令：
问答列表 - 查看所有已学习的问答
问答查询 <关键词> - 搜索包含关键词的问答

管理员指令：
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

def read_user_groups():
    """读取管理员和超级用户组"""
    manage_users = []
    super_users = []
    
    if os.path.exists(MANAGE_USER_INI):
        with open(MANAGE_USER_INI, 'r', encoding='utf-8') as f:
            manage_users = [line.strip() for line in f if line.strip()]
    
    if os.path.exists(SUPER_USER_INI):
        with open(SUPER_USER_INI, 'r', encoding='utf-8') as f:
            super_users = [line.strip() for line in f if line.strip()]
    
    return manage_users, super_users

def is_admin(user_id: str) -> bool:
    """检查用户是否有管理员权限"""
    try:
        manage_users, super_users = read_user_groups()
        return user_id in manage_users or user_id in super_users
    except Exception as e:
        print(f"[Text_Parser] 读取用户组配置失败: {str(e)}")
        return False

# 修改 on_message 函数
async def on_message(event, actions, Manager, Segments):
    message = str(event.message).strip()
    user_id = str(event.user_id)
    
    # 处理查看问答列表的命令
    if message == "问答列表":
        if not qa_data:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("还没有学习任何问答"))
            )
            return True
            
        # 按问题排序并格式化输出
        qa_list = sorted(qa_data.keys())
        response = "已学习的问答：\n" + "\n".join(qa_list)
        
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(response))
        )
        return True
        
    # 处理问答查询命令
    elif message.startswith("问答查询 "):
        keyword = message[5:].strip()
        if not keyword:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("请输入要搜索的关键词"))
            )
            return True
            
        # 搜索包含关键词的问答
        matches = [q for q in qa_data.keys() if keyword in q]
        if not matches:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"未找到包含关键词 '{keyword}' 的问答"))
            )
            return True
            
        response = f"包含关键词 '{keyword}' 的问答：\n" + "\n".join(matches)
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(response))
        )
        return True

    # 处理需要管理员权限的命令
    if message.startswith(("学习 ", "忘记 ")):
        if not is_admin(user_id):
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("只有管理员才能修改问答内容"))
            )
            return True
            
        # 处理学习命令
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
        
        # 处理忘记命令
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
    
    # 处理问答匹配
    elif message in qa_data:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(qa_data[message]))
        )
        return True
    
    return False
