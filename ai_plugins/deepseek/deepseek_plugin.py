"""
DeepSeek AI插件
基于DeepSeek API的AI对话插件
"""
import openai
import json
from typing import AsyncGenerator, Dict, Any
import sys
import os
# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_ai_plugin import BaseAIPlugin
from Tools.AI_tools import StreamSplitter


class DeepSeekPlugin(BaseAIPlugin):
    """DeepSeek AI插件"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'deepseek-chat')
        self.base_url = config.get('base_url', 'https://api.deepseek.com/')
        self.history_limit = config.get('history_limit', 7)
        
        # 设置OpenAI客户端
        if self.api_key:
            openai.api_key = self.api_key
            openai.base_url = self.base_url
            openai.default_headers = {"x-foo": "true"}
    
    @property
    def plugin_name(self) -> str:
        return "deepseek"
    
    @property
    def plugin_description(self) -> str:
        return "DeepSeek深度思考AI模型，提供高质量的对话体验"
    
    @property
    def plugin_version(self) -> str:
        return "1.0.0"
    
    @property
    def trigger_keywords(self) -> list[str]:
        return ["deepseek"]
    
    @property
    def display_name(self) -> str:
        return "DeepSeek深度思考"
    
    @property
    def supports_streaming(self) -> bool:
        return True
    
    async def process_message(self, 
                            message: str,
                            user_id: str,
                            system_prompt: str = "",
                            images: list = None,
                            **kwargs) -> AsyncGenerator[str, None]:
        """处理用户消息"""
        try:
            if not self.api_key:
                yield "错误：DeepSeek API密钥未配置"
                return
            
            # 获取群组ID和用户名
            group_id = kwargs.get('group_id', 'default')
            user_name = kwargs.get('user_name', f'User_{user_id}')
            
            # 添加用户消息到记忆
            self.add_to_memory(user_id, group_id, user_name, message, "user")
            
            # 获取记忆上下文
            bot_name = kwargs.get('bot_name', 'AI')
            memory_context = self.get_memory_context(user_id, group_id, system_prompt, bot_name)
            
            # 调用API
            chat_completion = openai.chat.completions.create(
                messages=memory_context,
                model=self.model,
                stream=True,
                extra_body={
                    "return_reasoning": True
                }
            )
            
            # 处理流式响应
            splitter = StreamSplitter()
            full_response = ""
            
            for message_chunk, _ in splitter.split_stream(chat_completion, 'openai'):
                full_response += message_chunk
                yield message_chunk
            
            # 添加AI回复到记忆（使用统一的bot_name）
            if full_response.strip():
                self.add_to_memory(user_id, group_id, bot_name, full_response, "assistant")
            
        except Exception as e:
            yield f"DeepSeek API调用错误: {str(e)}"