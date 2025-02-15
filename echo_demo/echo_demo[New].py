from Hyper import Manager, Segments

# 插件元数据
TRIGGHT_KEYWORD = "xiaoyi"
HELP_MESSAGE = """复读插件
使用方法：xiaoyi <要复读的内容>"""

__name__ = "EchoDemo"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

async def on_message(event, actions, Manager, Segments):
    user_message = str(event.message)
    
    if user_message.startswith("xiaoyi"):
        # 移除开头的 "xiaoyi" 并去除前后空格
        echo_message = user_message[6:].strip()
        
        if echo_message:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"echo {echo_message}"))
            )
            return True
    
    return False  # 如果不是以 "xiaoyi" 开头的消息,返回 False
