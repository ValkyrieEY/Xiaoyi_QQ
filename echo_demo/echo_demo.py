async def on_message(event, actions):
    user_message = str(event.message)
    
    if user_message.startswith("xiaoyi"):
        # 移除开头的 "xiaoyi" 并去除前后空格
        echo_message = user_message[6:].strip()
        
        if echo_message:
            return f"echo {echo_message}"
    
    return None  # 如果不是以 "xiaoyi" 开头的消息,返回 None
