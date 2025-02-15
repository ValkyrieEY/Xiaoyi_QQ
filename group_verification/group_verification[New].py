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
/设置验证操作 <ban/kick> - 设置验证失败处理方式"""

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

@Logic.ErrorHandler().handle_async
async def on_message(event, actions, Manager, Segments):
    global pending_verifications, DEFAULT_ACTION

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
        if message.startswith("/设置验证操作"):
            if await is_admin(user_id, group_id, actions):
                action = message.split()[-1].lower()
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
            else:
                await actions.send(
                    group_id=group_id,
                    message=Manager.Message(Segments.Text("只有管理员才能更改此设置。"))
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
    group_member_info = await actions.get_group_member_info(group_id=group_id, user_id=user_id)
    return group_member_info.data.raw['role'] in ['owner', 'admin']