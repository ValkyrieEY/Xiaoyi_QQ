import re
import os
import asyncio
import time
from datetime import datetime
from typing import Optional
from playwright.async_api import async_playwright
from Hyper import Configurator, Manager, Segments

# 插件元数据
TRIGGER_KEYWORD = "Any"  # 设置为 Any 以处理所有消息中的链接
HELP_MESSAGE = """网页截图插件
功能：
1. 自动检测消息中的URL并生成截图
2. !ws url <URL> - 手动触发截图
3. !ws help - 显示此帮助"""

__name__ = "WebScreenshot"
__version__ = "1.2.0"
__author__ = "Xiaoyi"

# ...existing code for configuration and WebScreenshot class...

# URL匹配正则表达式
URL_PATTERN = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'


def normalize_url(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url


class Screenshot:
    def __init__(self):
        self.command_prefix = TRIGGER_KEYWORD

    async def take_screenshot(self, url, user_id):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            filepath = f"screenshots/{user_id}_{int(time.time())}.png"
            await page.screenshot(path=filepath)
            await browser.close()
            return filepath

    async def cleanup(self):
        # Add any necessary cleanup code here
        pass


screenshot = Screenshot()


async def on_message(event, actions, Manager, Segments):
    message = str(event.message)
    user_id = str(event.user_id)
    
    # 处理命令
    if message.startswith("!ws"):
        cmd_parts = message[3:].strip().split()
        if not cmd_parts:
            return False
            
        cmd = cmd_parts[0]
        
        if cmd == "help":
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(
                    "网页截图插件帮助：\n"
                    "1. 直接发送含URL的消息即可自动截图\n"
                    "2. !ws url <URL> - 手动触发截图\n"
                    "3. !ws help - 显示此帮助"
                ))
            )
            return True
            
        elif cmd == "url" and len(cmd_parts) > 1:
            url = normalize_url(cmd_parts[1])
            if not re.match(URL_PATTERN, url):
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text("无效的URL格式"))
                )
                return True
            
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("正在截图中，请稍候..."))
            )
            
            filepath = await screenshot.take_screenshot(url, user_id)
            if filepath:
                try:
                    await actions.send(
                        group_id=event.group_id,
                        message=Manager.Message([
                            Segments.Text("网页截图完成"),
                            Segments.Image(filepath)
                        ])
                    )
                finally:
                    # 发送后删除文件
                    os.remove(filepath)
            else:
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text("操作太频繁或截图失败，请稍后重试"))
                )
            return True
    
    # 自动检测消息中的URL并截图
    urls = re.findall(URL_PATTERN, message)
    if urls:
        # 去重并限制数量
        urls = list(set(normalize_url(url) for url in urls))[:2]  # 每条消息最多处理2个URL
        
        for url in urls:
            filepath = await screenshot.take_screenshot(url, user_id)
            if not filepath:
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text("操作太频繁或服务器繁忙，请稍后再试"))
                )
                continue
                
            try:
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message([
                        Segments.Text("网页截图完成"),
                        Segments.Image(filepath)
                    ])
                )
            finally:
                os.remove(filepath)
        return True
    
    return False

# 当插件被卸载时清理资源
async def on_unload():
    await screenshot.cleanup()
