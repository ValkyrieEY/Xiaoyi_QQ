import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from Hyper import Configurator, Manager, Segments

# 插件元数据
TRIGGHT_KEYWORD = "!bl"
HELP_MESSAGE = """黑名单管理系统
命令：
!bl status - 查看系统状态
!bl help - 显示帮助信息
管理员命令：
!bl add <QQ号> <原因> - 添加黑名单
!bl remove <QQ号> - 移除黑名单
!bl addadmin <QQ号> - 添加管理员
!bl removeadmin <QQ号> - 移除管理员
!bl toggle - 开关黑名单系统"""

__name__ = "BlacklistManager"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

# 配置文件路径
BLACKLIST_FILE = os.path.join(os.path.dirname(__file__), "blacklist_data.json")
ADMIN_FILE = os.path.join(os.path.dirname(__file__), "xiaoyi_admins.json")

class BlacklistSystem:
    def __init__(self):
        # 确保配置目录存在
        config_dir = os.path.dirname(__file__)
        os.makedirs(config_dir, exist_ok=True)

        # 初始化默认配置
        self.default_admin = "2477194503"  # 替换为你的QQ号
        
        # 初始化黑名单数据
        self.blacklist: Dict[str, dict] = self.load_or_create_data(
            BLACKLIST_FILE,
            {},
            "黑名单数据文件已创建"
        )
        
        # 初始化管理员数据
        self.admins = self.load_or_create_data(
            ADMIN_FILE,
            {
                "admins": [self.default_admin],
                "enabled": True,
                "system_enabled": True
            },
            "管理员配置文件已创建"
        )
        
        self.command_prefix = "!bl"

    def load_or_create_data(self, file_path: str, default_data: dict, create_message: str) -> dict:
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=2)
                print(f"[BlacklistManager] {create_message}")
                return default_data
            except Exception as e:
                print(f"[BlacklistManager] 创建配置文件失败: {str(e)}")
                return default_data
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[BlacklistManager] 读取配置文件失败: {str(e)}")
            return default_data

    def save_data(self, file_path: str, data: dict) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[BlacklistManager] 保存数据失败: {str(e)}")
            return False

    def add_admin(self, admin_id: str) -> bool:
        if admin_id not in self.admins["admins"]:
            self.admins["admins"].append(admin_id)
            return self.save_data(ADMIN_FILE, self.admins)
        return False

    def remove_admin(self, admin_id: str) -> bool:
        if admin_id in self.admins["admins"]:
            self.admins["admins"].remove(admin_id)
            return self.save_data(ADMIN_FILE, self.admins)
        return False

    def is_admin(self, user_id: str) -> bool:
        return user_id in self.admins["admins"]

    def add_to_blacklist(self, user_id: str, reason: str, operator_id: str) -> bool:
        self.blacklist[user_id] = {
            "reason": reason,
            "add_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": operator_id
        }
        return self.save_data(BLACKLIST_FILE, self.blacklist)

    def remove_from_blacklist(self, user_id: str) -> bool:
        if user_id in self.blacklist:
            del self.blacklist[user_id]
            return self.save_data(BLACKLIST_FILE, self.blacklist)
        return False

    def is_blacklisted(self, user_id: str) -> Optional[dict]:
        return self.blacklist.get(user_id)

    def is_system_enabled(self) -> bool:
        return self.admins.get("system_enabled", True) and self.admins.get("enabled", True)

    def toggle_system(self, enabled: bool) -> bool:
        self.admins["enabled"] = enabled
        return self.save_data(ADMIN_FILE, self.admins)

blacklist_system = BlacklistSystem()

async def on_message(event, actions, Manager, Segments):
    user_id = str(event.user_id)
    message = str(event.message)
    
    # 检查是否在黑名单中
    blacklist_info = blacklist_system.is_blacklisted(user_id)
    if blacklist_info and blacklist_system.is_system_enabled():
        try:
            # 获取用户信息
            user_info = await actions.get_stranger_info(int(user_id))
            nickname = user_info.data.raw.get('nickname', '未知昵称')
            operator_info = await actions.get_stranger_info(int(blacklist_info['operator']))
            operator_nickname = operator_info.data.raw.get('nickname', '未知昵称')
            
            response = f"⚠️警告：此用户在黑名单中\n"
            response += f"用户：{nickname} ({user_id})\n"
            response += f"原因：{blacklist_info['reason']}\n"
            response += f"添加时间：{blacklist_info['add_time']}\n"
            response += f"操作者：{operator_nickname} ({blacklist_info['operator']})"
            
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(response)))
        except Exception as e:
            print(f"[BlacklistManager] 获取用户信息失败: {str(e)}")

    # 处理命令
    if not message.startswith(blacklist_system.command_prefix):
        return False

    cmd_parts = message[len(blacklist_system.command_prefix):].strip().split()
    if not cmd_parts:
        return False

    cmd = cmd_parts[0]
    is_admin = blacklist_system.is_admin(user_id)

    # 始终可用的命令
    if cmd == "status":
        response = "黑名单系统状态\n"
        response += f"系统状态：{'启用' if blacklist_system.is_system_enabled() else '禁用'}\n"
        response += f"黑名单数量：{len(blacklist_system.blacklist)}\n"
        response += f"管理员数量：{len(blacklist_system.admins['admins'])}"
        if is_admin:
            response += "\n管理员列表：" + ", ".join(blacklist_system.admins["admins"])
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(response)))
        return True

    elif cmd == "help":
        response = "黑名单系统命令帮助\n"
        response += "普通命令：\n"
        response += f"{blacklist_system.command_prefix} status - 查看系统状态（始终可用）\n"
        response += f"{blacklist_system.command_prefix} help - 显示此帮助\n"
        if is_admin:
            response += "\n管理员命令：\n"
            response += f"{blacklist_system.command_prefix} add <QQ号> <原因> - 添加黑名单\n"
            response += f"{blacklist_system.command_prefix} remove <QQ号> - 移除黑名单\n"
            response += f"{blacklist_system.command_prefix} addadmin <QQ号> - 添加管理员\n"
            response += f"{blacklist_system.command_prefix} removeadmin <QQ号> - 移除管理员\n"
            response += f"{blacklist_system.command_prefix} toggle - 开关黑名单系统"
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(response)))
        return True

    # 管理员命令
    if not is_admin:
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("你没有权限执行此操作")))
        return True

    if cmd == "toggle":
        enabled = not blacklist_system.admins["enabled"]
        if blacklist_system.toggle_system(enabled):
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"黑名单系统已{'启用' if enabled else '禁用'}")))
        else:
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("切换系统状态失败")))
        return True

    # 如果系统未启用，其他管理员命令不可用
    if not blacklist_system.is_system_enabled():
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("黑名单系统当前已禁用")))
        return True

    if cmd == "add" and len(cmd_parts) >= 3:
        target_id = cmd_parts[1]
        reason = " ".join(cmd_parts[2:])
        if blacklist_system.add_to_blacklist(target_id, reason, user_id):
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"已将用户 {target_id} 添加至黑名单\n原因：{reason}")))
        else:
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("添加黑名单失败")))
        return True

    elif cmd == "remove" and len(cmd_parts) == 2:
        target_id = cmd_parts[1]
        if blacklist_system.remove_from_blacklist(target_id):
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"已将用户 {target_id} 从黑名单中移除")))
        else:
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("移除黑名单失败")))
        return True

    elif cmd == "addadmin" and len(cmd_parts) == 2:
        target_id = cmd_parts[1]
        if blacklist_system.add_admin(target_id):
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"已将用户 {target_id} 添加为管理员")))
        else:
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("添加管理员失败")))
        return True

    elif cmd == "removeadmin" and len(cmd_parts) == 2:
        target_id = cmd_parts[1]
        if blacklist_system.remove_admin(target_id):
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"已将用户 {target_id} 移除管理员权限")))
        else:
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("移除管理员失败")))
        return True

    return True