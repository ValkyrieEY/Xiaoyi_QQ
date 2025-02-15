import json
import os
import time
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional
from Hyper import Configurator, Manager, Segments

# 插件元数据
TRIGGHT_KEYWORD = "!as"
HELP_MESSAGE = """刷屏检测系统命令：
!as status - 查看系统状态
!as set check_time <秒数> - 设置检测时间窗口
!as set max_messages <数量> - 设置最大消息数
!as toggle - 开关系统
!as clear <QQ号> - 清除指定用户的警告记录
!as help - 显示此帮助"""

__name__ = "AntiSpamPlugin"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

# 配置文件路径
ANTISPAM_CONFIG = os.path.join(os.path.dirname(__file__), "antispam_config.json")
ADMIN_FILE = os.path.join(os.path.dirname(__file__), "xiaoyi_admins.json")

# 添加文件路径常量
MANAGE_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Manage_User.ini")
SUPER_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Super_User.ini")

def read_user_groups():
    """读取管理员和超级用户组"""
    manage_users = []
    super_users = []
    
    # 读取 Manage_User.ini
    if os.path.exists(MANAGE_USER_INI):
        with open(MANAGE_USER_INI, 'r', encoding='utf-8') as f:
            manage_users = [line.strip() for line in f if line.strip()]
    
    # 读取 Super_User.ini
    if os.path.exists(SUPER_USER_INI):
        with open(SUPER_USER_INI, 'r', encoding='utf-8') as f:
            super_users = [line.strip() for line in f if line.strip()]
    
    return manage_users, super_users

class AntiSpamSystem:
    def __init__(self):
        # 确保配置目录存在
        config_dir = os.path.dirname(__file__)
        os.makedirs(config_dir, exist_ok=True)

        # 加载配置
        self.config = self.load_or_create_data(
            ANTISPAM_CONFIG,
            {
                "check_time": 10,  # 默认检测时间窗口(秒)
                "max_messages": 10,  # 默认最大消息数
                "enabled": True,  # 系统开关
                "warn_records": {}  # 警告记录
            },
            "刷屏检测配置文件已创建"
        )

        # 加载管理员配置(与黑名单系统共用)
        self.admins = self.load_or_create_data(
            ADMIN_FILE,
            {
                "admins": [],
                "enabled": True,
                "system_enabled": True
            },
            "管理员配置文件已创建"
        )

        # 用于记录用户消息
        self.user_messages: Dict[str, List[float]] = defaultdict(list)
        self.command_prefix = "!as"  # antispam的命令前缀

    def load_or_create_data(self, file_path: str, default_data: dict, create_message: str) -> dict:
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=2)
                print(f"[AntiSpamPlugin] {create_message}")
                return default_data
            except Exception as e:
                print(f"[AntiSpamPlugin] 创建配置文件失败: {str(e)}")
                return default_data
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[AntiSpamPlugin] 读取配置文件失败: {str(e)}")
            return default_data

    def save_config(self) -> bool:
        try:
            with open(ANTISPAM_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[AntiSpamPlugin] 保存配置失败: {str(e)}")
            return False

    def is_admin(self, user_id: str) -> bool:
        """检查是否是管理员"""
        # 检查内部管理员列表
        if user_id in self.admins["admins"]:
            return True
        
        try:
            # 读取外部用户组配置
            manage_users, super_users = read_user_groups()
            
            # 检查用户是否在任一用户组中
            if user_id in manage_users or user_id in super_users:
                return True
        except Exception as e:
            print(f"[AntiSpamPlugin] 读取用户组配置失败: {str(e)}")
        
        return False

    def is_public_command(self, cmd: str) -> bool:
        """检查是否是公开命令"""
        return cmd in ["status", "help"]

    def check_spam(self, user_id: str) -> tuple[bool, int]:
        """检查用户是否刷屏"""
        current_time = time.time()
        messages = self.user_messages[user_id]
        
        # 移除过期的消息记录
        check_time = self.config["check_time"]
        messages = [msg_time for msg_time in messages if current_time - msg_time <= check_time]
        self.user_messages[user_id] = messages
        
        # 添加新消息
        messages.append(current_time)
        
        # 检查是否超过限制
        return len(messages) > self.config["max_messages"], len(messages)

    def add_warning(self, user_id: str):
        """添加警告记录"""
        if user_id not in self.config["warn_records"]:
            self.config["warn_records"][user_id] = {
                "count": 0,
                "last_warn_time": None
            }
        
        self.config["warn_records"][user_id]["count"] += 1
        self.config["warn_records"][user_id]["last_warn_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_config()

spam_system = AntiSpamSystem()

async def on_message(event, actions, Manager, Segments):
    user_id = str(event.user_id)
    message = str(event.message)
    
    # 处理命令
    if message.startswith(spam_system.command_prefix):
        cmd_parts = message[len(spam_system.command_prefix):].strip().split()
        if not cmd_parts:
            return False

        cmd = cmd_parts[0]
        
        # 检查是否是公开命令
        if not spam_system.is_public_command(cmd) and not spam_system.is_admin(user_id):
            await actions.send(
                group_id=event.group_id, 
                message=Manager.Message(Segments.Text("你没有权限执行此操作"))
            )
            return True

        if cmd == "status":
            response = "刷屏检测系统状态：\n"
            response += f"系统状态：{'启用' if spam_system.config['enabled'] else '禁用'}\n"
            response += f"检测时间：{spam_system.config['check_time']}秒\n"
            response += f"最大消息数：{spam_system.config['max_messages']}条\n"
            response += f"已记录警告：{len(spam_system.config['warn_records'])}人"
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(response)))
            return True

        elif cmd == "set":
            if len(cmd_parts) != 3:
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("格式错误！使用方法：!as set <check_time/max_messages> <值>")))
                return True
            
            param = cmd_parts[1]
            try:
                value = int(cmd_parts[2])
                if value <= 0:
                    raise ValueError
            except ValueError:
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("参数必须是正整数！")))
                return True

            if param == "check_time":
                spam_system.config["check_time"] = value
            elif param == "max_messages":
                spam_system.config["max_messages"] = value
            else:
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("未知参数！可用参数：check_time, max_messages")))
                return True

            if spam_system.save_config():
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"设置成功！当前配置：\n检测时间：{spam_system.config['check_time']}秒\n最大消息数：{spam_system.config['max_messages']}条")))
            else:
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("设置失败！")))
            return True

        elif cmd == "toggle":
            spam_system.config["enabled"] = not spam_system.config["enabled"]
            if spam_system.save_config():
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"系统已{'启用' if spam_system.config['enabled'] else '禁用'}")))
            else:
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("切换状态失败！")))
            return True

        elif cmd == "clear":
            if len(cmd_parts) != 2:
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("格式错误！使用方法：!as clear <QQ号>")))
                return True
            
            target_id = cmd_parts[1]
            if target_id in spam_system.config["warn_records"]:
                del spam_system.config["warn_records"][target_id]
                if spam_system.save_config():
                    await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"已清除 {target_id} 的警告记录")))
                else:
                    await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("清除失败或用户无警告记录")))
            return True

        elif cmd == "help":
            response = "刷屏检测系统命令帮助：\n"
            response += "!as status - 查看系统状态\n"
            response += "!as set check_time <秒数> - 设置检测时间窗口\n"
            response += "!as set max_messages <数量> - 设置最大消息数\n"
            response += "!as toggle - 开关系统\n"
            response += "!as clear <QQ号> - 清除指定用户的警告记录\n"
            response += "!as help - 显示此帮助"
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(response)))
            return True

        return False

    # 检查刷屏
    if spam_system.config["enabled"] and not spam_system.is_admin(user_id):
        is_spam, msg_count = spam_system.check_spam(user_id)
        if is_spam:
            # 获取警告次数
            warn_count = spam_system.config["warn_records"].get(user_id, {}).get("count", 0)
            last_warn_time = spam_system.config["warn_records"].get(user_id, {}).get("last_warn_time", "从未")
            
            # 添加新警告
            spam_system.add_warning(user_id)
            
            try:
                nickname = (await actions.get_stranger_info(int(user_id))).data.raw['nickname']
                response = f"⚠️ 刷屏警告\n"
                response += f"用户：{nickname} ({user_id})\n"
                response += f"{spam_system.config['check_time']}秒内发送了{msg_count}条消息\n"
                response += f"这是第{warn_count + 1}次警告\n"
                response += f"上次警告时间：{last_warn_time}"
                
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text(response))
                )
            except Exception as e:
                print(f"[AntiSpamPlugin] 发送警告失败: {str(e)}")

    return False