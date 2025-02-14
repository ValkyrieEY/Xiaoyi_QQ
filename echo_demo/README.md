# Echo Demo 插件文档

## 插件信息
- 名称: Echo Demo
- 版本: 1.0.0
- 简介: 一个简单的消息回声插件

## 功能说明
Echo Demo 是一个基础的消息回声插件,当收到以 "xiaoyi" 开头的消息时,会将消息内容作为回声返回。

## 工作原理
插件监听所有消息事件,当消息以 "xiaoyi" 开头时:
1. 移除消息开头的 "xiaoyi" 关键词
2. 去除消息前后的空格
3. 在消息前添加 "echo" 并返回

## 使用方法

### 基本用法
发送格式:
```
xiaoyi 你的消息
```

### 使用示例
用户输入:
```
xiaoyi 你好世界
```

插件回复:
```
echo 你好世界
```

## 代码实现
```python
async def on_message(event, actions):
    user_message = str(event.message)
    
    if user_message.startswith("xiaoyi"):
        # 移除开头的 "xiaoyi" 并去除前后空格
        echo_message = user_message[6:].strip()
        
        if echo_message:
            return f"echo {echo_message}"
    
    return None  # 如果不是以 "xiaoyi" 开头的消息,返回 None
```

## 特性说明
- 异步处理消息
- 自动过滤非触发消息
- 智能去除多余空格
- 保持消息原始格式

## 注意事项
1. 触发词 "xiaoyi" 必须在消息开头
2. 消息内容不能为空
3. 触发词后需要有空格

## 错误处理
- 空消息将被忽略
- 非触发消息返回 None
- 自动处理消息类型转换

## 依赖项
- Python 3.7+
- asyncio
- Hyper 框架