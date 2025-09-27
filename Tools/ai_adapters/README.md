# AI适配器系统

这是一个模块化的AI适配器系统，允许用户轻松地开发和使用不同的AI模型适配器。

## 特性

- 模块化设计，易于扩展
- 支持多种记忆范围（全局、用户、群组）
- 统一的接口，便于切换不同的AI模型
- 配置管理
- 流式响应支持

## 快速开始

1. 安装依赖：
```bash
pip install google-generativeai
```

2. 创建配置文件：
```python
from Tools.ai_adapters.config import AIAdapterConfig

config = AIAdapterConfig()
config.set_adapter_config("gemini", {
    "api_key": "your_api_key",
    "model_name": "gemini-pro"
})
```

3. 使用适配器：
```python
from Tools.ai_adapters.factory import AIAdapterFactory
from Tools.ai_adapters.base import Message, MemoryScope

# 创建适配器实例
adapter = AIAdapterFactory.create_adapter("gemini", config.get_adapter_config("gemini"))

# 设置记忆范围
adapter.set_memory_scope(MemoryScope.USER)

# 生成响应
messages = [
    Message(role="user", content="你好！")
]

async for response in adapter.generate_response(
    messages,
    context_id="user_123"
):
    print(response)
```

## 开发新的适配器

要开发新的AI适配器，只需继承`BaseAIAdapter`类并实现必要的方法：

```python
from Tools.ai_adapters.base import BaseAIAdapter, Message

class MyCustomAdapter(BaseAIAdapter):
    def __init__(self, config):
        super().__init__(config)
        # 初始化你的AI模型
        
    async def generate_response(self, messages, stream=True, **kwargs):
        # 实现响应生成逻辑
        pass
        
    async def get_embedding(self, text):
        # 实现文本嵌入逻辑
        pass
        
    async def clear_memory(self, context_id):
        # 实现记忆清除逻辑
        pass
```

然后注册你的适配器：

```python
from Tools.ai_adapters.factory import AIAdapterFactory

AIAdapterFactory.register_adapter("my_custom", MyCustomAdapter)
```

## 记忆管理

系统支持三种记忆范围：

- `MemoryScope.GLOBAL`: 全局记忆，所有用户共享
- `MemoryScope.USER`: 用户级别记忆，每个用户独立
- `MemoryScope.GROUP`: 群组级别记忆，每个群组独立

可以通过`set_memory_scope`方法设置记忆范围：

```python
adapter.set_memory_scope(MemoryScope.USER)
```

## 配置管理

配置管理器支持：

- 设置/获取适配器配置
- 设置/获取默认适配器
- 自动保存配置到文件

```python
config = AIAdapterConfig()

# 设置适配器配置
config.set_adapter_config("gemini", {
    "api_key": "your_api_key",
    "model_name": "gemini-pro"
})

# 设置默认适配器
config.set_default_adapter("gemini")
```

## 注意事项

1. 确保在使用适配器前正确配置API密钥
2. 根据实际需求选择合适的记忆范围
3. 处理流式响应时注意内存使用
4. 定期清理不需要的记忆数据 