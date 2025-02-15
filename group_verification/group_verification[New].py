import os
import asyncio
import random
import string
from Hyper import Configurator, Events, Listener, Manager, Segments
from Hyper.Utils import Logic

# 插件元数据
TRIGGHT_KEYWORD = "Any"  # 需要监听所有消息来处理验证
HELP_MESSAGE = """群聊验证系统
功能：
- 新成员加入自动发送验证码
- 验证超时自动处理
管理员命令：
/设置验证操作 <ban/kick> - 设置验证失败处理方式
/设置验证时间 <秒数> - 设置验证超时时间
/设置验证码长度 <长度> - 设置验证码长度
/设置禁言时间 <秒数> - 设置禁言时长"""

__name__ = "GroupVerification"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

# 首先初始化配置管理器
if not hasattr(Configurator, 'cm'):
    Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

# 存储待验证用户信息的字典
pending_verifications = {}

# 验证设置
VERIFICATION_TIMEOUT = 60  # 验证超时时间（秒）
VERIFICATION_LENGTH = 6  # 验证码长度
DEFAULT_ACTION = "ban"  # 默认操作：'ban' 禁言 或 'kick' 踢出
BAN_DURATION = 300  # 禁言时长（秒）

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

@Logic.ErrorHandler().handle_async
async def on_message(event, actions, Manager, Segments):
    global pending_verifications, DEFAULT_ACTION, VERIFICATION_TIMEOUT, VERIFICATION_LENGTH, BAN_DURATION

    # 处理新成员加入
    if isinstance(event, Events.GroupMemberIncreaseEvent):
        verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=VERIFICATION_LENGTH))
        user_id = event.user_id
        group_id = event.group_id

        await actions.send(
            group_id=group_id, 
            message=Manager.Message([
                Segments.At(user_id),
                Segments.Text(f" 欢迎加入群聊！请在 {VERIFICATION_TIMEOUT} 秒内发送以下验证码：{verification_code}")
            ])
        )

        pending_verifications[user_id] = {
            "code": verification_code,
            "group_id": group_id,
            "timestamp": asyncio.get_event_loop().time()
        }

        asyncio.create_task(verify_timeout(user_id, group_id, actions))
        return True

    # 处理验证消息
    elif isinstance(event, Events.GroupMessageEvent):
        user_id = event.user_id
        group_id = event.group_id
        message = str(event.message)

        # 处理管理员命令
        if message.startswith("/设置"):
            if not await is_admin(user_id, group_id, actions):
                await actions.send(
                    group_id=group_id,
                    message=Manager.Message(Segments.Text("只有管理员才能更改此设置。"))
                )
                return True

            cmd_parts = message.split()
            if len(cmd_parts) != 3:
                await actions.send(
                    group_id=group_id,
                    message=Manager.Message(Segments.Text("命令格式错误。"))
                )
                return True

            try:
                value = int(cmd_parts[2])
                if message.startswith("/设置验证时间"):
                    if value < 10 or value > 300:
                        await actions.send(
                            group_id=group_id,
                            message=Manager.Message(Segments.Text("验证时间必须在 10-300 秒之间。"))
                        )
                        return True
                    VERIFICATION_TIMEOUT = value
                    await actions.send(
                        group_id=group_id,
                        message=Manager.Message(Segments.Text(f"验证超时时间已设置为: {value}秒"))
                    )

                elif message.startswith("/设置验证码长度"):
                    if value < 4 or value > 8:
                        await actions.send(
                            group_id=group_id,
                            message=Manager.Message(Segments.Text("验证码长度必须在 4-8 位之间。"))
                        )
                        return True
                    VERIFICATION_LENGTH = value
                    await actions.send(
                        group_id=group_id,
                        message=Manager.Message(Segments.Text(f"验证码长度已设置为: {value}位"))
                    )

                elif message.startswith("/设置禁言时间"):
                    if value < 60 or value > 2592000:  # 最长30天
                        await actions.send(
                            group_id=group_id,
                            message=Manager.Message(Segments.Text("禁言时间必须在 60秒-30天 之间。"))
                        )
                        return True
                    BAN_DURATION = value
                    await actions.send(
                        group_id=group_id,
                        message=Manager.Message(Segments.Text(f"验证失败禁言时长已设置为: {value}秒"))
                    )

                elif message.startswith("/设置验证操作"):
                    # 保持原有的验证操作设置代码
                    action = cmd_parts[2].lower()
                    if action in ["ban", "kick"]:
                        DEFAULT_ACTION = action
                        await actions.send(
                            group_id=group_id,
                            message=Manager.Message(Segments.Text(f"验证失败操作已设置为: {action}"))
                        )
                    else:
                        await actions.send(
                            group_id=group_id,
                            message=Manager.Message(Segments.Text("无效的操作。请使用 'ban' 或 'kick'。"))
                        )

            except ValueError:
                await actions.send(
                    group_id=group_id,
                    message=Manager.Message(Segments.Text("请输入有效的数字。"))
                )
            return True

        # 处理验证码验证
        if user_id in pending_verifications and pending_verifications[user_id]["group_id"] == group_id:
            if message.strip() == pending_verifications[user_id]["code"]:
                del pending_verifications[user_id]
                await actions.send(
                    group_id=group_id,
                    message=Manager.Message([
                        Segments.At(user_id),
                        Segments.Text(" 验证成功！欢迎加入群聊。")
                    ])
                )
            else:
                await actions.send(
                    group_id=group_id,
                    message=Manager.Message([
                        Segments.At(user_id),
                        Segments.Text(" 验证失败，请重新输入正确的验证码。")
                    ])
                )
            return True

    return False

async def verify_timeout(user_id: int, group_id: int, actions: Listener.Actions):
    await asyncio.sleep(VERIFICATION_TIMEOUT)
    if user_id in pending_verifications:
        del pending_verifications[user_id]
        if DEFAULT_ACTION == "ban":
            await actions.set_group_ban(group_id=group_id, user_id=user_id, duration=BAN_DURATION)
            await actions.send(group_id=group_id, message=Manager.Message(
                Segments.At(user_id),
                Segments.Text(f" 验证超时，已被禁言 {BAN_DURATION} 秒。")
            ))
        elif DEFAULT_ACTION == "kick":
            await actions.set_group_kick(group_id=group_id, user_id=user_id)
            await actions.send(group_id=group_id, message=Manager.Message(
                Segments.Text(f"用户 {user_id} 验证超时，已被踢出群聊。")
            ))

async def is_admin(user_id: int, group_id: int, actions: Listener.Actions) -> bool:
    # 检查群管理员权限
    group_member_info = await actions.get_group_member_info(group_id=group_id, user_id=user_id)
    is_group_admin = group_member_info.data.raw['role'] in ['owner', 'admin']
    
    try:
        # 从 ini 文件读取用户组
        manage_users, super_users = read_user_groups()
        
        # 检查用户是否在任一用户组中
        is_privileged_user = (str(user_id) in manage_users) or (str(user_id) in super_users)
        
        return is_group_admin or is_privileged_user
    except Exception as e:
        print(f"[GroupVerification] 读取用户组配置失败: {str(e)}")
        return is_group_admin