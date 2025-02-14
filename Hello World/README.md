# Hello World 插件文档

## 插件信息
- 名称: Hello World
- 版本: 1.0.0
- 作者: Xiaoyi

## 功能简介
这是一个简单的示例插件，当检测到消息中包含 "hello" 关键词时（不区分大小写），会回复 "Hello, world! 🌍"。

## 实现细节

### 触发条件
- 消息中包含 "hello" 文本（不区分大小写）
- 在群聊中生效

### 响应内容
固定回复:
```
Hello, world! 🌍
```

## 代码实现
```python
async def on_message(event, actions):
    user_message = str(event.message)

    if "hello" in user_message.lower():
        response = "Hello, world! 🌍"
        await actions.send(
            group_id=event.group_id, 
            message=Manager.Message(Segments.Text(response))
        )
        return None

    return None
```

## 功能说明
1. 监听所有消息事件
2. 将消息转换为小写进行关键词匹配
3. 使用异步方式发送回复
4. 支持 emoji 表情

## 使用方法
在群聊中发送包含 "hello" 的消息即可触发回复，例如：
- hello
- Hello World
- HELLO
- 你好 hello

## 依赖项
- Hyper 框架
- Manager 模块
- Segments 模块
- Events 模块

## 技术特点
- 异步处理
- 大小写不敏感
- Unicode 支持
- 群聊消息支持

## 注意事项
1. 插件只响应群聊消息
2. 不需要特定的命令前缀
3. 任何包含 "hello" 的消息都会触发
4. 每次触发只回复一次

## 开发信息
- 语言: Python
- 框架: Hyper
- 异步支持: 是
- 消息类型: 文本