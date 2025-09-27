"""
Google Gemini AI插件
基于Google Gemini API的AI对话插件，支持图片处理
"""
from typing import AsyncGenerator, Dict, Any
import sys
import os
# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_ai_plugin import BaseAIPlugin
from Tools.GoogleAI import genai, Context, Parts, Roles


class GeminiPlugin(BaseAIPlugin):
    """Google Gemini AI插件"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.model_name = config.get('model', 'gemini-2.0-flash-thinking-exp-01-21')
        self.generation_config = config.get('generation_config', {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        })
        
        # 配置Gemini
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        # 上下文管理器
        self.context_managers = {}
    
    @property
    def plugin_name(self) -> str:
        return "gemini"
    
    @property
    def plugin_description(self) -> str:
        return "Google Gemini多模态AI模型，支持文本和图片理解"
    
    @property
    def plugin_version(self) -> str:
        return "1.0.0"
    
    @property
    def trigger_keywords(self) -> list[str]:
        return ["gemini"]
    
    @property
    def display_name(self) -> str:
        return "Gemini视觉理解"
    
    @property
    def supports_images(self) -> bool:
        return True
    
    @property
    def supports_streaming(self) -> bool:
        return True
    
    def get_context_manager(self, user_id: str, group_id: str = "default"):
        """获取用户的上下文管理器"""
        context_key = f"{group_id}_{user_id}"
        if context_key not in self.context_managers:
            # 创建模型和工具（如果需要）
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            tools = []  # 可以根据需要添加工具
            
            # 创建上下文
            context = Context(self.api_key, model, tools=tools)
            self.context_managers[context_key] = context
        
        return self.context_managers[context_key]
    
    async def build_message_content(self, message: str, images: list = None):
        """构建消息内容"""
        content = [Parts.text(message)]
        
        if images and self.supports_images:
            for image in images:
                # 这里需要根据实际的图片处理逻辑来实现
                # 假设images是图片URL或base64数据的列表
                content.append(Parts.image(image))
        
        return content
    
    async def process_message(self, 
                            message: str,
                            user_id: str,
                            system_prompt: str = "",
                            images: list = None,
                            group_id: str = "default",
                            **kwargs) -> AsyncGenerator[str, None]:
        """处理用户消息"""
        try:
            if not self.api_key:
                yield "错误：Gemini API密钥未配置"
                return
            
            # 获取用户名
            user_name = kwargs.get('user_name', f'User_{user_id}')
            
            # 添加用户消息到记忆
            self.add_to_memory(user_id, group_id, user_name, message, "user")
            
            # 获取上下文管理器（兼容旧系统）
            context_manager = self.get_context_manager(user_id, group_id)
            
            # 构建消息内容
            message_content = await self.build_message_content(message, images)
            
            # 创建模型（如果需要系统提示词）
            # 为Gemini增强系统提示词
            bot_name = kwargs.get('bot_name', 'AI')
            mode = self.get_memory_mode(user_id)
            
            if mode.value == "global":
                # 全局记忆模式下，检查是否有全局预设
                global_preset = self.get_global_preset(group_id)
                if global_preset:
                    # 使用全局预设
                    try:
                        import prerequisites.prerequisite as presets_tool
                        presets = presets_tool.read_presets()
                        for preset_id, preset_data in presets.items():
                            if preset_data.get("name") == global_preset:
                                preset_path = os.path.join(presets_tool.PRESET_DIR, preset_data["path"])
                                if os.path.exists(preset_path):
                                    with open(preset_path, 'r', encoding='utf-8') as f:
                                        global_system_prompt = f.read()
                                        # 替换变量
                                        global_system_prompt = global_system_prompt.replace("{self.bot_name}", bot_name)
                                        global_system_prompt = global_system_prompt.replace("{self.event_user}", "")
                                        
                                        enhanced_prompt = (f"{global_system_prompt}\n\n"
                                                         "注意：当前为群组全局记忆模式，请根据消息中的用户信息区分不同的发言者。"
                                                         "用户信息格式为：[用户名(QQ:用户ID) 时间] 消息内容")
                                        break
                                break
                        else:
                            # 如果找不到全局预设，使用默认系统提示
                            enhanced_prompt = (f"{system_prompt or ''}\n\n"
                                             "注意：当前为群组全局记忆模式，请根据消息中的用户信息区分不同的发言者。"
                                             "用户信息格式为：[用户名(QQ:用户ID) 时间] 消息内容")
                    except Exception as e:
                        print(f"加载全局预设失败: {e}")
                        enhanced_prompt = (f"{system_prompt or ''}\n\n"
                                         "注意：当前为群组全局记忆模式，请根据消息中的用户信息区分不同的发言者。"
                                         "用户信息格式为：[用户名(QQ:用户ID) 时间] 消息内容")
                else:
                    # 如果没有设置全局预设，使用默认系统提示
                    enhanced_prompt = (f"{system_prompt or ''}\n\n"
                                     "注意：当前为群组全局记忆模式，请根据消息中的用户信息区分不同的发言者。"
                                     "用户信息格式为：[用户名(QQ:用户ID) 时间] 消息内容")
            else:
                enhanced_prompt = (f"{system_prompt or ''}\n\n"
                                 "注意：当前为个人记忆模式，你正在与单个用户进行对话。")
            
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                system_instruction=enhanced_prompt or None,
            )
            
            # 生成响应
            response_stream = context_manager.gen_content(Roles.User(*message_content))
            
            # 处理流式响应
            full_response = ""
            async for chunk in response_stream:
                if hasattr(chunk, 'text') and chunk.text:
                    full_response += chunk.text
                    yield chunk.text
                elif isinstance(chunk, str):
                    full_response += chunk
                    yield chunk
            
            # 添加AI回复到记忆（使用统一的bot_name）
            if full_response.strip():
                self.add_to_memory(user_id, group_id, bot_name, full_response, "assistant")
                    
        except Exception as e:
            yield f"Gemini API调用错误: {str(e)}"