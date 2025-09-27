from pathlib import Path
from typing import List, Optional, Literal

class Config:
    # 命令配置
    COMMAND: List[str] = ["运行状态", "状态", "zt", "yxzt", "status"]
    NEED_AT: bool = False  # 是否需要@机器人
    ONLY_SUPERUSER: bool = False  # 是否仅超级用户可用
    
    # 系统信息收集配置
    COLLECT_INTERVAL: int = 2  # 收集间隔（秒）
    IGNORE_DISK_PARTS: List[str] = []  # 忽略的磁盘分区
    IGNORE_NETWORK_INTERFACES: List[str] = ["^lo(op)?\\d*$", "^Loopback"]  # 忽略的网络接口
    PROCESS_LIMIT: int = 5  # 显示进程数量限制
    IGNORE_PROCESSES: List[str] = ["^System Idle Process$"]  # 忽略的进程
    
    # 网络测试配置
    TEST_SITES: List[dict] = [
        {"name": "百度", "url": "https://www.baidu.com/"},
        {"name": "Google", "url": "https://www.google.com/", "use_proxy": True}
    ]
    TEST_TIMEOUT: int = 5  # 网络测试超时时间（秒）
    
    # 样式配置
    DEFAULT_BG_PATH: Path = Path(__file__).parent / "assets" / "default_bg.webp"
    DEFAULT_AVATAR_PATH: Path = Path(__file__).parent / "assets" / "default_avatar.webp"
    
    # 模板配置
    TEMPLATE: Literal["default", "simple", "modern"] = "default"  # 使用的模板
    TEMPLATE_CONFIG: dict = {
        "default": {
            "width": 800,
            "height": 600,
            "padding": 20,
            "line_height": 30,
            "font_size": 24,
            "bg_color": (255, 255, 255),
            "text_color": (0, 0, 0),
            "section_color": (0, 0, 0),
            "show_avatar": True,
            "show_bg": True
        },
        "simple": {
            "width": 600,
            "height": 400,
            "padding": 15,
            "line_height": 25,
            "font_size": 20,
            "bg_color": (240, 240, 240),
            "text_color": (50, 50, 50),
            "section_color": (100, 100, 100),
            "show_avatar": False,
            "show_bg": False
        },
        "modern": {
            "width": 900,
            "height": 700,
            "padding": 25,
            "line_height": 35,
            "font_size": 26,
            "bg_color": (30, 30, 30),
            "text_color": (200, 200, 200),
            "section_color": (100, 200, 255),
            "show_avatar": True,
            "show_bg": True
        }
    }
    
    # 缓存配置
    CACHE_SIZE: int = 1  # 缓存大小

config = Config() 