import re
import os
import asyncio
import time
from datetime import datetime
from typing import Optional
from playwright.async_api import async_playwright
from Hyper import Configurator

# 首先初始化配置管理器
if not hasattr(Configurator, 'cm'):
    Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

# 然后再导入其他 Hyper 模块
from Hyper import Manager, Segments

__name__ = "WebScreenshot"
__version__ = "1.2.0"
__author__ = "Xiaoyi"

# 配置
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# URL正则匹配模式，同时支持带协议和不带协议的URL
URL_PATTERN = r'(?:https?:\/\/)?(?:[\w-]+\.)+[a-z]{2,}(?:\/[^\s]*)?'

def normalize_url(url: str) -> str:
    """规范化 URL，确保有正确的协议头"""
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url

class WebScreenshot:
    def __init__(self):
        self.browser = None
        self.context = None
        self.playwright = None
        self.command_prefix = "!ws"  # 截图命令前缀
        
        # 性能优化配置
        self.config = {
            "max_concurrent": 1,      # 最大并发截图数
            "min_interval": 5,        # 两次截图最小间隔(秒)
            "timeout": 15000,         # 截图超时时间(毫秒)
            "max_height": 15000,      # 最大截图高度(像素)
            "viewport_width": 1280,   # 视口宽度
            "viewport_height": 720,    # 视口高度
            "image_quality": 70       # 图片质量(1-100)
        }
        
        # 限流器
        self._semaphore = asyncio.Semaphore(self.config["max_concurrent"])
        self._last_screenshot = {}    # 记录每个用户的最后截图时间

    async def init_browser(self):
        """初始化浏览器"""
        try:
            if not self.playwright:
                self.playwright = await async_playwright().start()
            if not self.browser:
                self.browser = await self.playwright.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-gpu',
                        '--disable-dev-shm-usage',
                        '--disable-setuid-sandbox',
                        '--no-sandbox',
                        '--disable-extensions',
                    ]
                )
            if not self.context:
                self.context = await self.browser.new_context(
                    viewport={
                        "width": self.config["viewport_width"],
                        "height": self.config["viewport_height"]
                    },
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
            return True
        except Exception as e:
            print(f"[WebScreenshot] 浏览器初始化失败: {str(e)}")
            await self.cleanup()
            return False

    async def cleanup(self):
        """清理浏览器资源"""
        try:
            if self.context:
                await self.context.close()
                self.context = None
            if self.browser:
                await self.browser.close()
                self.browser = None
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
        except Exception as e:
            print(f"[WebScreenshot] 清理资源失败: {str(e)}")

    async def take_screenshot(self, url: str, user_id: str) -> Optional[str]:
        """对网页进行长截图"""
        # 检查冷却时间
        current_time = time.time()
        if user_id in self._last_screenshot:
            if current_time - self._last_screenshot[user_id] < self.config["min_interval"]:
                return None

        async with self._semaphore:  # 使用信号量限制并发
            try:
                # 记录本次截图时间
                self._last_screenshot[user_id] = current_time
                
                if not await self.init_browser():
                    return None

                page = await self.context.new_page()
                try:
                    # 设置超时和其他选项
                    page.set_default_timeout(self.config["timeout"])
                    
                    # 访问页面
                    await page.goto(url, wait_until="domcontentloaded")
                    
                    # 获取并限制页面高度
                    page_height = min(
                        await page.evaluate("""
                            Math.min(
                                Math.max(
                                    document.body.scrollHeight,
                                    document.documentElement.scrollHeight,
                                    document.body.offsetHeight,
                                    document.documentElement.offsetHeight
                                ),
                                15000
                            )
                        """),
                        self.config["max_height"]
                    )
                    
                    # 设置视口
                    await page.set_viewport_size({
                        "width": self.config["viewport_width"],
                        "height": page_height
                    })
                    
                    # 生成文件名
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                    filepath = os.path.join(SCREENSHOT_DIR, filename)
                    
                    # 截图
                    await page.screenshot(
                        path=filepath,
                        full_page=True,
                        type="jpeg",
                        quality=self.config["image_quality"]
                    )
                    
                    return filepath
                    
                finally:
                    await page.close()
                    
            except Exception as e:
                print(f"[WebScreenshot] 截图失败: {str(e)}")
                return None

screenshot = WebScreenshot()

async def on_message(event, actions):
    message = str(event.message)
    user_id = str(event.user_id)
    
    # 处理命令
    if message.startswith(screenshot.command_prefix):
        cmd_parts = message[len(screenshot.command_prefix):].strip().split()
        if not cmd_parts:
            return None
            
        cmd = cmd_parts[0]
        
        if cmd == "help":
            response = "网页截图插件帮助：\n"
            response += "1. 直接发送含URL的消息即可自动截图\n"
            response += "2. !ws url <URL> - 手动触发截图\n"
            response += "3. !ws help - 显示此帮助"
            return Manager.Message(Segments.Text(response))
            
        elif cmd == "url" and len(cmd_parts) > 1:
            url = normalize_url(cmd_parts[1])
            if not re.match(URL_PATTERN, url):
                return Manager.Message(Segments.Text("无效的URL格式"))
            
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("正在截图中，请稍候..."))
            )
            
            filepath = await screenshot.take_screenshot(url, user_id)
            if filepath:
                try:
                    await actions.send(
                        group_id=event.group_id,
                        message=Manager.Message(
                            Segments.Text(f"网页截图完成"),
                            Segments.Image(filepath)
                        )
                    )
                finally:
                    # 发送后删除文件
                    os.remove(filepath)
            else:
                return Manager.Message(Segments.Text("操作太频繁或截图失败，请稍后重试"))
            
        return None
    
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
                    message=Manager.Message(
                        Segments.Text(f"网页截图完成"),
                        Segments.Image(filepath)
                    )
                )
            finally:
                os.remove(filepath)
    
    return None

# 当插件被卸载时清理资源
async def on_unload():
    await screenshot.cleanup()