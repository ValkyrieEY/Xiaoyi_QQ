# 🔌 插件开发指南

## 📖 插件架构

小依QQ使用基于HypeR_Bot框架的插件化架构，支持热重载和动态加载。每个插件都是独立的Python模块。

## 🛠️ 创建基础插件

### 简单插件模板
```python
# plugins/HelloWorld.py
from Hyper import Configurator
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

TRIGGHT_KEYWORD = "你好，世界"
HELP_MESSAGE = f"{Configurator.cm.get_cfg().others["reminder"]}你好，世界 —> 仅仅就是一句 Hello world 🤔？"

async def on_message(event, actions, Manager, Segments):
    await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("Hello, world! 🌍")))
    return True
```

### 插件基本结构
每个插件都需要包含以下核心元素：

1. **导入配置管理器**
```python
from Hyper import Configurator
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())
```

2. **定义触发关键词**
```python
TRIGGHT_KEYWORD = "关键词"  # 触发插件的关键词
# 或者使用 "Any" 表示接收所有消息
TRIGGHT_KEYWORD = "Any"
```

3. **定义帮助信息**
```python
HELP_MESSAGE = f"{Configurator.cm.get_cfg().others['reminder']}命令 —> 功能描述"
```

4. **定义主处理函数**
```python
async def on_message(event, actions, Manager, Segments, **kwargs):
    # 插件逻辑
    return True  # 或 False/None
```

## 📚 插件类型

### 1. 命令触发插件
```python
from Hyper import Configurator
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

TRIGGHT_KEYWORD = "天气"
HELP_MESSAGE = f"{Configurator.cm.get_cfg().others['reminder']}天气 (城市) —> 查询指定城市的天气"

async def on_message(event, actions, Manager, Segments, order=None):
    # order 参数包含去掉触发词后的内容
    city = order.strip() if order else "北京"
    
    # 查询天气逻辑
    weather_info = f"{city}今天天气晴朗"
    
    await actions.send(
        group_id=event.group_id,
        message=Manager.Message(Segments.Text(weather_info))
    )
    return True
```

### 2. 全局监听插件
```python
from Hyper import Configurator
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

TRIGGHT_KEYWORD = "Any"  # 监听所有消息
HELP_MESSAGE = "自动回复插件 - 监听特定关键词并自动回复"

async def on_message(event, actions, Manager, Segments, user_message=None):
    # user_message 包含用户的完整消息
    message_text = str(user_message) if user_message else str(event.message)
    
    if "早上好" in message_text:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(
                Segments.At(event.user_id),
                Segments.Text(" 早上好！")
            )
        )
        return True
    
    return None  # 不处理其他消息
```

### 3. 复杂功能插件（带数据存储）
```python
import json
import time
from dataclasses import dataclass
from Hyper import Configurator
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

TRIGGHT_KEYWORD = "签到"
HELP_MESSAGE = f"{Configurator.cm.get_cfg().others['reminder']}签到 —> 每日签到获取积分"

@dataclass
class UserData:
    points: int = 0
    last_checkin: int = 0
    
    def can_checkin(self) -> bool:
        return time.time() - self.last_checkin > 86400  # 24小时

# 数据存储
user_data = {}

async def on_message(event, actions, Manager, Segments):
    user_id = str(event.user_id)
    
    # 加载用户数据
    if user_id not in user_data:
        user_data[user_id] = UserData()
    
    user = user_data[user_id]
    
    if user.can_checkin():
        user.points += 10
        user.last_checkin = int(time.time())
        
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(
                Segments.At(event.user_id),
                Segments.Text(f" 签到成功！获得10积分，当前积分：{user.points}")
            )
        )
    else:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(
                Segments.At(event.user_id),
                Segments.Text(" 今天已经签到过了！")
            )
        )
    
    return True
```

## 🎯 高级功能

### 文件夹式插件结构
对于复杂插件，可以使用文件夹结构：

```
plugins/
├── MyPlugin/
│   ├── __init__.py
│   ├── setup.py          # 主插件文件
│   ├── core.py           # 核心逻辑
│   └── utils.py          # 工具函数
```

**setup.py** (插件入口):
```python
import plugins.MyPlugin.core as Core
from Hyper import Configurator
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

TRIGGHT_KEYWORD = "复杂功能"
HELP_MESSAGE = f"{Configurator.cm.get_cfg().others['reminder']}复杂功能 —> 执行复杂的功能"

async def on_message(event, actions, Manager, Segments, **kwargs):
    result = await Core.handle_request(event, actions, Manager, Segments, **kwargs)
    return result
```

### 消息类型处理

#### 处理不同消息段
```python
async def on_message(event, actions, Manager, Segments):
    for segment in event.message:
        if isinstance(segment, Segments.At):
            # 处理@消息
            at_user = segment.qq
            print(f"用户@了：{at_user}")
        
        elif isinstance(segment, Segments.Image):
            # 处理图片消息
            image_url = segment.url
            print(f"收到图片：{image_url}")
        
        elif isinstance(segment, Segments.Text):
            # 处理文本消息
            text_content = segment.text
            print(f"文本内容：{text_content}")
```

#### 发送不同类型消息
```python
async def on_message(event, actions, Manager, Segments):
    # 发送纯文本
    await actions.send(
        group_id=event.group_id,
        message=Manager.Message(Segments.Text("纯文本消息"))
    )
    
    # 发送@消息
    await actions.send(
        group_id=event.group_id,
        message=Manager.Message(
            Segments.At(event.user_id),
            Segments.Text(" 你好！")
        )
    )
    
    # 发送图片
    await actions.send(
        group_id=event.group_id,
        message=Manager.Message(
            Segments.Image("file:///path/to/image.jpg")
        )
    )
    
    # 发送回复消息
    await actions.send(
        group_id=event.group_id,
        message=Manager.Message(
            Segments.Reply(event.message_id),
            Segments.Text("这是回复消息")
        )
    )
    
    return True
```

### 事件类型判断
```python
from Hyper.Events import *

async def on_message(event, actions, Manager, Segments):
    if isinstance(event, GroupMessageEvent):
        # 群消息事件
        print(f"群消息来自群：{event.group_id}")
    
    elif isinstance(event, PrivateMessageEvent):
        # 私聊消息事件  
        print(f"私聊消息来自：{event.user_id}")
    
    # 处理消息...
    return True
```

## 🔧 插件配置

### 使用配置管理器
```python
from Hyper import Configurator

# 获取配置
config = Configurator.cm.get_cfg()
bot_name = config.others["bot_name"]
reminder = config.others["reminder"]

# 在插件中使用
HELP_MESSAGE = f"{reminder}命令 —> 让{bot_name}执行某个功能"
```

### 权限管理
```python
async def on_message(event, actions, Manager, Segments, ROOT_User=None, Super_User=None):
    user_id = str(event.user_id)
    
    # 检查ROOT权限
    if ROOT_User and user_id in ROOT_User:
        # 执行管理员功能
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("管理员功能执行成功"))
        )
        return True
    
    # 检查Super权限
    elif Super_User and user_id in Super_User:
        # 执行超级用户功能
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("超级用户功能执行成功"))
        )
        return True
    
    else:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("权限不足"))
        )
        return False
```

## 📝 插件规范

### 文件命名规范
- 简单插件：`PluginName.py`
- 复杂插件：`PluginName/setup.py`
- 私有插件：以`[XY]`前缀开头
- 停用插件：以`d_`前缀开头

### 代码规范
```python
# 标准导入顺序
import sys  # 系统库
import json  # 标准库
import httpx  # 第三方库
from Hyper import Configurator  # 框架库

# 配置管理器初始化（必需）
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

# 插件元数据（必需）
TRIGGHT_KEYWORD = "关键词"
HELP_MESSAGE = "帮助信息"

# 主处理函数（必需）
async def on_message(event, actions, Manager, Segments, **kwargs):
    # 插件逻辑
    return True  # 成功处理返回True，未处理返回None/False
```

### 错误处理
```python
async def on_message(event, actions, Manager, Segments):
    try:
        # 插件逻辑
        result = await some_async_function()
        
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(f"结果：{result}"))
        )
        return True
        
    except Exception as e:
        # 错误处理
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(
                Segments.Text(f"插件执行出错：{str(e)}")
            )
        )
        return False
```

## 🧪 插件测试

### 本地测试
```python
# test_plugin.py
import asyncio
from unittest.mock import Mock

# 模拟事件和依赖
mock_event = Mock()
mock_event.group_id = "123456"
mock_event.user_id = "789012"
mock_event.message = [Mock()]

mock_actions = Mock()
mock_Manager = Mock()
mock_Segments = Mock()

# 测试插件
async def test_plugin():
    from plugins import YourPlugin
    
    result = await YourPlugin.on_message(
        mock_event, mock_actions, mock_Manager, mock_Segments
    )
    
    assert result is True
    print("插件测试通过")

# 运行测试
asyncio.run(test_plugin())
```

## 📦 可用参数和模块

### 常用参数 (详见Variables.md)
- `event` - 消息事件对象
- `actions` - 机器人操作接口
- `Manager` - 消息管理器
- `Segments` - 消息段类型
- `user_message` - 用户完整消息
- `order` - 去掉触发词的消息内容
- `reminder` - 机器人触发符号
- `bot_name` - 机器人名称
- `ROOT_User` - ROOT用户列表
- `Super_User` - 超级用户列表

### 可用模块
```python
# 常用内置模块
import asyncio, datetime, os, sys, random, time
import json, re, base64, urllib

# 第三方模块
import requests, aiohttp, httpx
from PIL import Image
import psutil

# 框架模块
from Hyper import Configurator, Listener, Events, Logger, Manager, Segments, Logic
```

## 🔗 相关资源

- [HypeR_Bot 文档](https://harcicyang.github.io/hyper-bot/)
- [OneBot 11 协议](https://github.com/botuniverse/onebot-11)
- [示例插件](../plugins/)
- [Variables.md](../Variables.md) - 完整参数列表