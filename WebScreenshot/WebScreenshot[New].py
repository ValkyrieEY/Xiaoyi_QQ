import re
import os
import asyncio
import time
import json
from datetime import datetime
from typing import Optional
from playwright.async_api import async_playwright
from Hyper import Configurator, Manager, Segments

# 插件元数据
TRIGGER_KEYWORD = "Any"  # 设置为 Any 以处理所有消息中的链接
HELP_MESSAGE = """网页截图插件
普通用户功能：
1. 自动检测消息中的URL并生成截图
2. !ws url <URL> - 手动触发截图
3. !ws help - 显示此帮助

管理员命令：
!ws toggle - 开关截图功能
!ws status - 查看功能状态"""

__name__ = "WebScreenshot"
__version__ = "1.2.0"
__author__ = "Xiaoyi"

# 添加文件路径常量
MANAGE_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Manage_User.ini")
SUPER_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Super_User.ini")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "webscreenshot_config.json")

# URL匹配正则表达式
URL_PATTERN = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'


def normalize_url(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url


def read_user_groups():
    """读取管理员和超级用户组"""
    manage_users = []
    super_users = []
    
    if os.path.exists(MANAGE_USER_INI):
        with open(MANAGE_USER_INI, 'r', encoding='utf-8') as f:
            manage_users = [line.strip() for line in f if line.strip()]
    
    if os.path.exists(SUPER_USER_INI):
        with open(SUPER_USER_INI, 'r', encoding='utf-8') as f:
            super_users = [line.strip() for line in f if line.strip()]
    
    return manage_users, super_users

def is_admin(user_id: str) -> bool:
    """检查用户是否有管理员权限"""
    try:
        manage_users, super_users = read_user_groups()
        return user_id in manage_users or user_id in super_users
    except Exception as e:
        print(f"[WebScreenshot] 读取用户组配置失败: {str(e)}")
        return False


class Screenshot:
    def __init__(self):
        self.command_prefix = TRIGGER_KEYWORD
        self.enabled = self.load_config().get('enabled', True)
    
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {'enabled': True}
    
    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'enabled': self.enabled}, f, indent=2)
            return True
        except:
            return False
    
    def toggle(self):
        self.enabled = not self.enabled
        self.save_config()
        return self.enabled

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
        
        # 管理员命令
        if cmd in ['toggle', 'status']:
            if not is_admin(user_id):
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text("只有管理员才能使用此命令"))
                )
                return True
                
            if cmd == 'toggle':
                enabled = screenshot.toggle()
                status = "启用" if enabled else "禁用"
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text(f"已{status}网页截图功能"))
                )
                return True
            
            elif cmd == 'status':
                status = "启用" if screenshot.enabled else "禁用"
                await actions.send(
                    group_id=event.group_id,
                    message=Manager.Message(Segments.Text(f"网页截图功能当前状态：{status}"))
                )
                return True
        
        # 检查功能是否启用
        if not screenshot.enabled:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("网页截图功能已被管理员禁用"))
            )
            return True
            
        # 处理普通命令
        if cmd == "help":
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(HELP_MESSAGE))
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
    
    # 检查功能是否启用后再处理自动URL检测
    if not screenshot.enabled:
        return False

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
