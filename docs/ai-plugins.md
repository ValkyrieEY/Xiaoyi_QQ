# 🤖 AI插件管理

## 🧠 AI架构概述

小依QQ支持多种AI模型，通过插件化架构实现灵活的AI服务集成。系统包含两层架构：

1. **AI适配器层** (`Tools/ai_adapters/`) - 底层AI服务接口
2. **AI插件层** (`ai_plugins/`) - 上层插件化封装

## 🔧 支持的AI模型

### DeepSeek
- **模型**: deepseek-chat
- **特点**: 代码理解能力强，逻辑推理优秀
- **支持流式输出**: 是
- **配置**: 需要DeepSeek API密钥

### Google Gemini
- **模型**: gemini-2.0-flash-thinking-exp-01-21
- **特点**: 多模态支持，图片理解能力强
- **支持图片**: 是
- **配置**: 需要Google AI Studio API密钥

### ChatGPT (OpenAI)
- **模型**: gpt-3.5-turbo-16k / gpt-4o-mini
- **特点**: 通用对话能力强，知识面广
- **配置**: 需要OpenAI API密钥

## 📝 配置文件

### AI插件主配置
```json
// config/ai_plugins_config.json
{
  "current_plugin": "deepseek",
  "plugins": {
    "deepseek": {
      "api_key": "sk-your-deepseek-api-key",
      "model": "deepseek-chat",
      "base_url": "https://api.deepseek.com/",
      "history_limit": 7,
      "enabled": true
    },
    "gemini": {
      "api_key": "your-gemini-api-key",
      "model": "gemini-2.0-flash-thinking-exp-01-21",
      "generation_config": {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain"
      },
      "enabled": true
    },
    "chatgpt": {
      "api_key": "sk-your-openai-api-key",
      "model_35": "gpt-3.5-turbo-16k",
      "model_4": "gpt-4o-mini",
      "default_model": "gpt-4o-mini",
      "enabled": true
    }
  }
}
```

### AI适配器配置
```json
// config/ai_adapters.json
{
  "default_adapter": "deepseek",
  "adapters": {
    "gemini": {
      "api_key": "YOUR_GEMINI_API_KEY",
      "model": "gemini-pro"
    },
    "deepseek": {
      "api_key": "sk-your-deepseek-api-key",
      "model": "deepseek-chat"
    }
  },
  "memory": {
    "scope": "conversation",
    "max_tokens": 1000
  }
}
```

## 🎛️ AI插件使用

### 触发关键词
每个AI插件都有对应的触发关键词：
- `deepseek` - 触发DeepSeek插件
- `gemini` - 触发Gemini插件
- `chatgpt` - 触发ChatGPT插件

### 使用方式
```bash
# 直接使用触发词
deepseek 请帮我写一个Python函数

# 或者在群聊中@机器人
@小依 gemini 这张图片是什么？[图片]
```

## 🧩 记忆管理系统

### 记忆模式
AI插件支持三种记忆模式：
- **PERSONAL**: 个人记忆模式，每个用户独立的对话记忆
- **GLOBAL**: 群组全局记忆，群组内共享的对话上下文
- **CONVERSATION**: 对话记忆模式，临时对话记忆

### 记忆操作
```python
# 记忆管理API
plugin.set_memory_mode(user_id, MemoryMode.PERSONAL)
plugin.add_to_memory(user_id, group_id, user_name, content, "user")
plugin.clear_memory(user_id, group_id)
plugin.get_memory_status(user_id, group_id)
```

### 全局预设管理
```python
# 设置群组全局预设
plugin.set_global_preset(group_id, "工作细胞")
plugin.get_global_preset(group_id)
plugin.clear_global_preset(group_id)
```

## 🛠️ 开发自定义AI插件

### 基础插件结构
```python
# ai_plugins/custom/custom_plugin.py
from typing import Dict, Any, AsyncGenerator
from ai_plugins.base_ai_plugin import BaseAIPlugin

class CustomAIPlugin(BaseAIPlugin):
    """自定义AI插件"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'custom-model')
    
    @property
    def plugin_name(self) -> str:
        return "custom"
    
    @property
    def plugin_description(self) -> str:
        return "自定义AI模型插件"
    
    @property
    def plugin_version(self) -> str:
        return "1.0.0"
    
    @property
    def trigger_keywords(self) -> list[str]:
        return ["custom", "自定义"]
    
    @property
    def display_name(self) -> str:
        return "自定义AI"
    
    @property
    def supports_images(self) -> bool:
        return False  # 是否支持图片处理
    
    @property
    def supports_streaming(self) -> bool:
        return True  # 是否支持流式输出
    
    async def process_message(self, 
                            message: str,
                            user_id: str,
                            system_prompt: str = "",
                            images: list = None,
                            **kwargs) -> AsyncGenerator[str, None]:
        """处理用户消息"""
        try:
            if not self.api_key:
                yield "错误：API密钥未配置"
                return
            
            # 获取群组ID和用户名
            group_id = kwargs.get('group_id', 'default')
            user_name = kwargs.get('user_name', f'User_{user_id}')
            
            # 添加用户消息到记忆
            self.add_to_memory(user_id, group_id, user_name, message, "user")
            
            # 获取记忆上下文
            bot_name = kwargs.get('bot_name', 'AI')
            memory_context = self.get_memory_context(user_id, group_id, system_prompt, bot_name)
            
            # 调用自定义AI API
            response = await self.call_custom_api(memory_context)
            
            # 流式返回结果
            for chunk in response:
                yield chunk
            
            # 添加AI回复到记忆
            full_response = ''.join(response)
            if full_response.strip():
                self.add_to_memory(user_id, group_id, bot_name, full_response, "assistant")
            
        except Exception as e:
            yield f"AI调用错误: {str(e)}"
    
    async def call_custom_api(self, messages):
        """调用自定义AI API"""
        # 实现您的AI API调用逻辑
        # 返回生成器以支持流式输出
        pass
```

### 插件注册
```python
# ai_plugins/__init__.py
from .custom.custom_plugin import CustomAIPlugin

def get_available_plugins():
    return {
        "custom": CustomAIPlugin
    }
```

### 插件配置
```json
// config/ai_plugins_config.json
{
  "current_plugin": "custom",
  "plugins": {
    "custom": {
      "api_key": "your-custom-api-key",
      "model": "custom-model",
      "base_url": "https://api.custom.com/",
      "enabled": true
    }
  }
}
```

## 📊 性能监控

### 插件状态查询
```python
# 获取插件信息
plugin_info = plugin.get_plugin_info()
print(plugin_info)
# 输出：
# {
#     "name": "deepseek",
#     "description": "DeepSeek深度思考AI模型",
#     "version": "1.0.0",
#     "display_name": "DeepSeek深度思考",
#     "trigger_keywords": ["deepseek"],
#     "supports_images": False,
#     "supports_streaming": True,
#     "enabled": True
# }
```

### 记忆状态监控
```python
# 获取记忆状态
memory_status = plugin.get_memory_status(user_id, group_id)
print(memory_status)
# 输出记忆使用情况、消息数量等信息
```

## 🚨 错误处理

### 常见问题

#### API密钥问题
```python
if not self.api_key:
    yield "错误：API密钥未配置，请检查配置文件"
    return
```

#### 网络连接问题
```python
try:
    response = await api_call()
except aiohttp.ClientError as e:
    yield f"网络连接错误: {str(e)}"
except asyncio.TimeoutError:
    yield "请求超时，请稍后重试"
```

#### 内存管理问题
```python
try:
    # 定期清理长期未使用的上下文
    if len(self.user_contexts) > 1000:
        # 清理逻辑
        self.cleanup_old_contexts()
except Exception as e:
    logger.error(f"内存清理失败: {e}")
```

## 🔗 相关资源

- [AI适配器系统文档](../Tools/ai_adapters/README.md)
- [记忆管理系统](../ai_plugins/memory_manager.py)
- [BaseAIPlugin基类](../ai_plugins/base_ai_plugin.py)
- [示例插件](../ai_plugins/deepseek/deepseek_plugin.py)