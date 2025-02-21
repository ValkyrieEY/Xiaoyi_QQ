# Hyper Bot 插件开发指南

本文档旨在帮助开发者理解和使用 Hyper Bot 框架进行插件开发。

## 基础概念

### 1. 插件结构
```python
# 必需的元数据
__name__ = "插件名称"
__version__ = "1.0.0"
__author__ = "作者名"

# 触发关键词
TRIGGHT_KEYWORD = "指令"  # 或 "Any" 处理所有消息

# 帮助信息
HELP_MESSAGE = """插件说明
命令列表：
/命令1 - 说明
/命令2 - 说明"""

# 消息处理函数
async def on_message(event, actions, Manager, Segments):
    # 插件逻辑
    return True  # 处理成功
    return False # 继续处理
```

### 2. 主要参数

#### Event 事件对象
```python
event.message    # 消息内容
event.user_id    # 发送者QQ号
event.group_id   # 群号
event.message_id # 消息ID
```

#### Actions 动作对象
```python
# 发送消息
await actions.send(
    group_id=group_id,
    message=Manager.Message([
        Segments.Text("文本"),
        Segments.At(user_id)
    ])
)

# 群管理
await actions.set_group_ban(group_id, user_id, duration)  # 禁言
await actions.delete_msg(message_id)                      # 撤回消息
await actions.get_group_member_info(group_id, user_id)    # 获取成员信息
```

#### 消息构建
```python
# 创建消息对象
message = Manager.Message([
    Segments.Text("文本"),    # 文本消息
    Segments.Image("路径"),   # 图片消息
    Segments.At(user_id),    # @某人
    Segments.Video("路径"),   # 视频消息
    Segments.Reply(msg_id)   # 回复消息
])
```

### 3. 事件类型
```python
Events.MessageEvent              # 消息事件基类
Events.PrivateMessageEvent      # 私聊消息
Events.GroupMessageEvent        # 群消息
Events.NoticeEvent             # 通知事件
Events.GroupMemberIncreaseEvent # 群成员增加
Events.GroupMemberDecreaseEvent # 群成员减少
Events.GroupMuteEvent          # 群禁言事件
# ...更多事件类型
```

### 4. 权限系统
```python
ROOT_User    # ROOT用户组
Super_User   # 超级用户组
Manage_User  # 管理员用户组
```

### 5. 全局变量
```python
bot_name      # 机器人名称
bot_name_en   # 机器人英文名称
version_name  # 项目版本号
reminder      # 机器人触发关键词
user_message  # 用户发送的消息
order         # 不含触发词的消息
```

### 6. 可用模块
```python
Configurator  # 配置管理
Logger        # 日志模块
Logic         # 逻辑处理
Manager       # 消息管理
Segments      # 消息段类型
Events        # 事件类型
```

## 插件开发示例

```python
# filepath: /plugins/example_plugin.py
from Hyper import Manager, Segments, Events

__name__ = "ExamplePlugin"
__version__ = "1.0.0"
__author__ = "YourName"

TRIGGHT_KEYWORD = "!cmd"
HELP_MESSAGE = """示例插件
命令：
!cmd test - 测试命令"""

async def on_message(event, actions, Manager, Segments):
    if not isinstance(event, Events.GroupMessageEvent):
        return False
        
    message = str(event.message)
    if message.startswith("!cmd test"):
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message([
                Segments.At(event.user_id),
                Segments.Text(" 测试成功！")
            ])
        )
        return True
        
    return False
```

## 最佳实践

1. **异常处理**
```python
try:
    # 危险操作
except Exception as e:
    print(f"[插件名] 错误: {str(e)}")
```

2. **消息处理**
```python
# 检查消息类型
if not isinstance(event, Events.GroupMessageEvent):
    return False

# 处理指令
cmd_parts = message.split()
if len(cmd_parts) < 2:
    return False
```

3. **权限检查**
```python
# 读取配置文件方式
MANAGE_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Manage_User.ini")
SUPER_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Super_User.ini")
```

4. **配置管理**
```python
# 使用 JSON 存储配置
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
```

## 注意事项

1. 所有异步操作都需要使用 `await`
2. 插件处理完成后返回 `True`，继续处理返回 `False`
3. 注意检查权限和异常处理
4. 使用有意义的变量名和注释
5. 遵循 PEP 8 编码规范

## 相关文档

- [Hyper Bot 官方文档](https://harcicyang.github.io/hyper-bot/)
- [Events 模块文档](https://harcicyang.github.io/hyper-bot/more/classes.html#events-模块)
- [Segments 模块文档](https://harcicyang.github.io/hyper-bot/more/classes.html#segments-模块)
