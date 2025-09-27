"""
ChatGPT AI插件
基于OpenAI ChatGPT API的AI对话插件
"""
from typing import AsyncGenerator, Dict, Any
import sys
import os
# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_ai_plugin import BaseAIPlugin
from Tools.SearchOnline import network_gpt as SearchOnline


class ChatGPTPlugin(BaseAIPlugin):
    """ChatGPT AI插件"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.model_35 = config.get('model_35', 'gpt-3.5-turbo-16k')
        self.model_4 = config.get('model_4', 'gpt-4o-mini')
        self.default_model = config.get('default_model', 'gpt-4o-mini')
    
    @property
    def plugin_name(self) -> str:
        return "chatgpt"
    
    @property
    def plugin_description(self) -> str:
        return "OpenAI ChatGPT模型，提供智能对话服务"
    
    @property
    def plugin_version(self) -> str:
        return "1.0.0"
    
    @property
    def trigger_keywords(self) -> list[str]:
        return ["chatgpt"]
    
    @property
    def display_name(self) -> str:
        return "ChatGPT智能对话"
    
    @property
    def supports_streaming(self) -> bool:
        return True
    
    def get_model_for_keyword(self, keyword: str) -> str:
        """根据关键词获取对应的模型"""
        if keyword in ["默认3.5", "Normal"]:
            return self.model_35
        elif keyword in ["默认4", "Net"]:
            return self.model_4
        else:
            return self.default_model
    
    async def process_message(self, 
                            message: str,
                            user_id: str,
                            system_prompt: str = "",
                            images: list = None,
                            trigger_keyword: str = "",
                            bot_name: str = "简儿",
                            **kwargs) -> AsyncGenerator[str, None]:
        """处理用户消息"""
        try:
            if not self.api_key:
                yield "错误：ChatGPT API密钥未配置"
                return
            
            # 获取群组ID和用户名
            group_id = kwargs.get('group_id', 'default')
            user_name = kwargs.get('user_name', f'User_{user_id}')
            
            # 添加用户消息到记忆
            self.add_to_memory(user_id, group_id, user_name, message, "user")
            
            # 根据触发关键词选择模型
            model_name = self.get_model_for_keyword(trigger_keyword)
            
            # 获取记忆上下文
            bot_name = kwargs.get('bot_name', 'AI')
            memory_context = self.get_memory_context(user_id, group_id, system_prompt, bot_name)
            
            # 使用OpenAI API直接调用（而不是SearchOnline）
            import openai
            openai.api_key = self.api_key
            
            # 调用API
            chat_completion = openai.chat.completions.create(
                messages=memory_context,
                model=model_name,
                stream=True
            )
            
            # 生成流式响应
            full_response = ""
            
            async for chunk in chat_completion:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # 添加AI回复到记忆（使用统一的bot_name）
            if full_response.strip():
                self.add_to_memory(user_id, group_id, bot_name, full_response, "assistant")
                    
        except Exception as e:
            yield f"ChatGPT API调用错误: {str(e)}"