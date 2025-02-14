from Hyper import Manager, Segments, Events

__name__ = "Hello World"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

async def on_message(event, actions):
    user_message = str(event.message)

    if "hello" in user_message.lower():
        response = "Hello, world! 🌍"
        await actions.send(
            group_id=event.group_id, 
            message=Manager.Message(Segments.Text(response))
        )
        # 返回 None 表示处理完成
        return None

    # 如果没有匹配的命令，返回 None 让其他插件处理
    return None