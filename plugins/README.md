# QQ机器人插件开发指南

## 📝 基础说明

### 快速上手
1. **开发**：通过Python开发插件，定义`on_message`函数并接收`event`和`actions`参数
2. **部署**：将`.py`文件放入插件文件夹即可自动加载
3. **管理**：发送"readplugins"命令查看插件加载状态
4. **禁用**：在插件文件名前添加"xyi_"前缀可禁用插件

### 框架初始化
```python
# 1. 导入配置管理器
from Hyper import Configurator

# 2. 初始化配置
Configurator.cm = Configurator.ConfigManager(
    Configurator.Config(file="config.json").load_from_file()
)
```

## 🔧 插件开发

### 基本结构
```python
async def on_message(event, actions):
    """
    处理群消息的主函数
    
    Args:
        event: 消息事件对象
        actions: 机器人行为控制对象
    
    Returns:
        str or None: 返回需要发送的消息,返回None则不发送
    """
    if str(event.message).startswith("插件前缀"):
        return "插件回复"
    return None
```

### 消息发送示例
```python
# 发送文本消息
await actions.send(
    group_id=event.group_id, 
    message=Manager.Message(Segments.Text("文本消息"))
)

# 发送图片
await actions.send(
    group_id=event.group_id,
    message=Manager.Message(Segments.Image("图片URL"))
)
```

## 📚 开发规范

### 插件命名规则
- 文件必须以`.py`结尾
- 使用描述性名称（如：`weather.py`, `translator.py`）
- 以`xyi_`开头的插件会被自动禁用

### 最佳实践

#### 1. 异常处理
```python
try:
    # 插件逻辑
except Exception as e:
    print(f"插件运行错误: {e}")
    return f"很抱歉,插件执行出错: {str(e)}"
```

#### 2. 权限控制
```python
if str(event.user_id) not in [Super_User, ROOT_User]:
    return "权限不足"
```

#### 3. 其他建议
- 实现消息频率限制（cooldown机制）
- 做好日志记录
- 避免无限循环
- 正确使用异步函数
- 保护敏感信息

## 🧪 测试指南

### 测试要点
1. 在测试群中进行功能验证
2. 使用`print`输出调试信息
3. 测试异常情况处理
4. 验证权限控制有效性

## ⚙️ 插件管理

### 管理功能
- **热重载**：使用`readplugins`命令
- **状态查看**：显示已加载/禁用/失败的插件
- **隔离运行**：插件在独立环境中执行

---

> 通过遵循以上指南，你可以开发出稳定可靠的插件来扩展机器人的功能。