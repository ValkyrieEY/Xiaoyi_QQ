import random
from Hyper import Manager, Segments, Events
from datetime import datetime

# 插件元数据
TRIGGHT_KEYWORD = "塞我口球"
HELP_MESSAGE = """自我禁言插件
指令：
塞我口球 - 获得一个随机时长的禁言（60-512秒）
特殊彩蛋：1%概率获得114514秒的禁言
注意：需要机器人具有群管理员权限才能使用"""

class SelfMute:
    def __init__(self):
        self.cooldowns = {}  # 用户冷却时间记录
        self.COOLDOWN_TIME = 300  # 冷却时间（秒）

    def is_on_cooldown(self, user_id: int) -> bool:
        """检查用户是否在冷却中"""
        now = datetime.now().timestamp()
        if user_id in self.cooldowns:
            if now - self.cooldowns[user_id] < self.COOLDOWN_TIME:
                return True
            del self.cooldowns[user_id]
        return False

    def set_cooldown(self, user_id: int):
        """设置用户冷却时间"""
        self.cooldowns[user_id] = datetime.now().timestamp()

mute_system = SelfMute()

async def on_message(event, actions, Manager, Segments):
    if not isinstance(event, Events.GroupMessageEvent):
        return False

    user_id = event.user_id
    group_id = event.group_id
    message = str(event.message)

    if TRIGGHT_KEYWORD in message:
        # 检查冷却时间
        if mute_system.is_on_cooldown(user_id):
            remaining = int(mute_system.COOLDOWN_TIME - 
                          (datetime.now().timestamp() - mute_system.cooldowns[user_id]))
            await actions.send(
                group_id=group_id,
                message=Manager.Message([
                    Segments.At(user_id),
                    Segments.Text(f" 你太贪心了！需要等待 {remaining} 秒后才能再次使用。")
                ])
            )
            return True

        try:
            # 检查机器人是否有禁言权限
            bot_info = await actions.get_group_member_info(group_id=group_id, user_id=actions.self_id)
            if bot_info.data.raw['role'] not in ['admin', 'owner']:
                await actions.send(
                    group_id=group_id,
                    message=Manager.Message(Segments.Text("抱歉，我没有禁言权限呢..."))
                )
                return True

            # 生成随机禁言时长
            if random.random() < 0.01:  # 1%概率
                duration = 114514
                special_msg = "恭喜触发彩蛋！"
            else:
                duration = random.randint(60, 512)
                special_msg = ""

            # 执行禁言 - 修改为 Hyper 框架的方式
            await actions.group_ban(
                group_id=group_id,
                user_id=user_id,
                time=duration
            )
            
            # 设置冷却时间
            mute_system.set_cooldown(user_id)

            # 发送回复
            await actions.send(
                group_id=group_id,
                message=Manager.Message([
                    Segments.At(user_id),
                    Segments.Text(f" {special_msg}你抖M是吧！来，张嘴。禁言时长：{duration}秒")
                ])
            )

        except Exception as e:
            await actions.send(
                group_id=group_id,
                message=Manager.Message([
                    Segments.At(user_id),
                    Segments.Text(f" 禁言失败了...可能是我权限不够或其他原因：{str(e)}")
                ])
            )

        return True

    return False