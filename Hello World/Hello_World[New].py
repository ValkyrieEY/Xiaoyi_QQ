from Hyper import Manager, Segments

# 插件元数据
TRIGGHT_KEYWORD = "hello"  # 触发关键词
HELP_MESSAGE = """Hello World 示例插件
功能：当消息中包含 hello 时回复打招呼"""

__name__ = "Hello World"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

async def on_message(event, actions, Manager, Segments):
    user_message = str(event.message)

    if "hello" in user_message.lower():
        await actions.send(
            group_id=event.group_id, 
            message=Manager.Message(Segments.Text("Hello, world! 🌍"))
        )
        return True  # 处理完成，阻止其他插件执行

    return False  # 未处理消息，允许其他插件继续处理
