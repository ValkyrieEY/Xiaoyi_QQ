import asyncio
from datetime import datetime
import logging
from Hyper import Configurator, Events, Listener, Manager, Segments
from Hyper.Utils import Logic

# 插件元数据
TRIGGHT_KEYWORD = "Any"  # 需要监听所有私聊消息
HELP_MESSAGE = """私聊消息转发插件
功能：自动将收到的私聊消息转发给管理员
仅管理员可见"""

__name__ = "PrivateMessageForwarder"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 从配置文件中获取管理员QQ号
config = Configurator.cm.get_cfg()
ADMIN_QQ = config.others.get("ADMIN_QQ", [])
if not ADMIN_QQ:
    logger.warning("ADMIN_QQ not set in config file. Please add ADMIN_QQ to your config.json")

# 调试模式
DEBUG = True

async def on_message(event, actions, Manager, Segments):
    if isinstance(event, Events.PrivateMessageEvent):
        logger.info(f"Received private message from user {event.user_id}")
        
        # 获取发送者信息
        sender_info = await actions.get_stranger_info(event.user_id)
        sender_name = sender_info.data.raw['nickname']
        sender_qq = event.user_id
        
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 构建转发消息
        forward_message = (
            f"收到私聊消息:\n"
            f"发送者: {sender_name}\n"
            f"QQ: {sender_qq}\n"
            f"时间: {current_time}\n"
            f"内容:\n"
        )
        
        # 处理文本消息
        text_content = str(event.message)
        if text_content:
            forward_message += text_content + "\n"
        
        # 处理图片消息
        try:
            for segment in event.message.segments:
                if isinstance(segment, Segments.Image):
                    forward_message += f"图片: {segment.url}\n"
        except Exception as e:
            logger.error(f"Failed to process image segments: {e}")
        
        # 转发消息给每个管理员
        for admin in ADMIN_QQ:
            try:
                logger.info(f"Attempting to forward message to admin {admin}")
                await actions.send(
                    user_id=admin, 
                    message=Manager.Message(Segments.Text(forward_message))
                )
                logger.info(f"Successfully forwarded message to admin {admin}")
            except Exception as e:
                logger.error(f"Failed to forward message to admin {admin}: {e}")

        # 回复发送者
        try:
            await actions.send(
                user_id=event.user_id, 
                message=Manager.Message(Segments.Text("您的消息已收到,我们会尽快回复您。"))
            )
            logger.info(f"Sent confirmation message to user {event.user_id}")
        except Exception as e:
            logger.error(f"Failed to send confirmation message to user {event.user_id}: {e}")

        if DEBUG:
            logger.debug(f"Full event data: {event}")
            logger.debug(f"Full actions data: {actions}")
        
        return True  # 阻止其他插件处理此私聊消息
    
    return False  # 非私聊消息继续由其他插件处理

logger.info("Private message forwarder plugin loaded successfully")