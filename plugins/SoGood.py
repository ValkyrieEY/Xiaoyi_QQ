import asyncio
import random
import time
import httpx
from random import randint
import dataclasses
import json
from Hyper import Configurator
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

TRIGGHT_KEYWORD = "Any"
HELP_MESSAGE = f'''{Configurator.cm.get_cfg().others["reminder"]}发电 (名字) —> 对某个人表达内心深处的诉求
       我今天棒不棒 —> 让{Configurator.cm.get_cfg().others["bot_name"]}来评评你今天表现怎么样'''

@dataclasses.dataclass
class UserInfo:
    goodness: int
    time: int

    @property
    def level(self) -> str:
        if 0 <= self.goodness <= 20:
            return "嗯~今天表现不乖，下次一定要听话哦"
        elif 20 < self.goodness <= 40:
            return "看着顺眼"
        elif 40 < self.goodness <= 60:
            return "亲爱的太棒啦！"
        elif 60 < self.goodness <= 80:
            return "来，抱一个~嗯~"
        else:
            return "👍_ _ _👍"

    @classmethod
    def build(cls) -> "UserInfo":
        return cls(randint(0, 100), int(time.time()))

users: dict[str, UserInfo] = {}
with open("./assets/quick.json", "r", encoding="utf-8") as f:
    words = json.load(f)["ele"]


async def on_message(event, actions, Manager, Events, Segments, reminder, order=None):
        # 如果是工作流调用，事件可能不是标准的GroupMessageEvent
        # 但仍然应该处理相关逻辑
        is_group_event = isinstance(event, Events.GroupMessageEvent) if hasattr(Events, 'GroupMessageEvent') else True
        
        # 如果不是群消息事件且不是工作流调用，直接返回
        if not is_group_event and hasattr(event, 'group_id') and not event.group_id:
            return None
        
        # 获取消息内容，优先使用order参数，然后是event.message
        message_str = ""
        if order:  # 工作流传递的order参数
            message_str = str(order)
        elif hasattr(event, 'message'):
            message_str = str(event.message)
        
        if "今天棒不棒" in message_str:
            name = ""
            uin = None
            
            if "我" in message_str:
                name = "\n你"
                uin = str(event.user_id) if hasattr(event, 'user_id') else None
            elif "@" in message_str and hasattr(event, 'message'):
                name = ""
                # 尝试从消息中获取@的用户
                if hasattr(event.message, '__iter__'):
                    for msg_part in event.message:
                        if isinstance(msg_part, Segments.At):
                            uin = msg_part.qq
                            break
            
            # 如果找不到用户ID，使用默认的发送者ID
            if not uin and hasattr(event, 'user_id'):
                uin = str(event.user_id)
                name = "\n你"
            
            if not uin:
                # 如果仍然没有用户ID，返回一个通用消息
                return "🎆 今天的表现很棒哦！继续加油！"

            if str(uin) not in users.keys():
                users[str(uin)] = UserInfo.build()

            # 尝试发送消息，如果发送失败则返回结果字符串
            try:
                msg = Manager.Message(
                    Segments.At(uin),
                    Segments.Text(
                        f" {name}今天的分数: {users[str(uin)].goodness}\n评级: {users[str(uin)].level}")
                )

                if hasattr(event, 'group_id') and event.group_id:
                    await actions.send(
                        group_id=event.group_id,
                        user_id=event.user_id if hasattr(event, 'user_id') else None,
                        message=msg
                    )
                    return True
                else:
                    # 如果没有group_id，可能是工作流调用，返回结果字符串
                    result_text = f"{name}今天的分数: {users[str(uin)].goodness}\n评级: {users[str(uin)].level}"
                    return result_text
                
            except Exception as e:
                # 发送失败，返回结果字符串
                result_text = f"{name}今天的分数: {users[str(uin)].goodness}\n评级: {users[str(uin)].level}"
                return result_text

        elif message_str.startswith(f"{reminder}发电"):
            uin = 0
            if hasattr(event, 'message') and hasattr(event.message, '__iter__'):
                for i in event.message:
                    if isinstance(i, Segments.At):
                        uin = i.qq
                        break
            if uin == 0:
                tag = message_str.replace(f"{reminder}发电", "", 1)
            else:
                tag = f"@{(await actions.get_stranger_info(uin)).data.raw["nickname"]}"

            word = random.choice(words).replace("{target_name}", tag)
            
            try:
                if hasattr(event, 'group_id') and event.group_id:
                    await actions.send(
                        group_id=event.group_id,
                        user_id=event.user_id if hasattr(event, 'user_id') else None,
                        message=Manager.Message(
                            Segments.Reply(event.message_id) if hasattr(event, 'message_id') else Segments.Text(""),
                            Segments.Text(word)
                        )
                    )
                    return True
                else:
                    # 如果没有group_id，可能是工作流调用，返回结果字符串
                    return word
                
            except Exception as e:
                # 发送失败，返回结果字符串
                return word
        
        # 如果没有匹配任何条件，返回None
        return None