"""
AI插件基类
定义了所有AI插件必须实现的接口规范
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, AsyncGenerator
import datetime
import sys
import os

ai_plugins_dir = os.path.dirname(os.path.abspath(__file__))
if ai_plugins_dir not in sys.path:
    sys.path.insert(0, ai_plugins_dir)

try:
    from memory_manager import AIMemoryManager, MemoryMode
except ImportError:
    try:
        from .memory_manager import AIMemoryManager, MemoryMode
    except ImportError:
        import importlib.util
        memory_manager_path = os.path.join(ai_plugins_dir, 'memory_manager.py')
        spec = importlib.util.spec_from_file_location("memory_manager", memory_manager_path)
        memory_manager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(memory_manager)
        AIMemoryManager = memory_manager.AIMemoryManager
        MemoryMode = memory_manager.MemoryMode


class BaseAIPlugin(ABC):
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = True
        self.user_contexts = {}
        self.memory_manager = AIMemoryManager()
        
    @property
    @abstractmethod
    def plugin_name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def plugin_description(self) -> str:
        pass
    
    @property
    @abstractmethod
    def plugin_version(self) -> str:
        pass
    
    @property
    @abstractmethod
    def trigger_keywords(self) -> list[str]:
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        pass
    
    @property
    def supports_images(self) -> bool:
        """是否支持图片处理"""
        return False
    
    @property
    def supports_streaming(self) -> bool:
        return False
    
    @abstractmethod
    async def process_message(self, 
                            message: str,
                            user_id: str,
                            system_prompt: str = "",
                            images: list = None,
                            **kwargs) -> AsyncGenerator[str, None]:
        pass
    
    def get_user_context(self, user_id: str) -> list:
        return self.user_contexts.get(user_id, [])
    
    def update_user_context(self, user_id: str, context: list):
        self.user_contexts[user_id] = context
    
    def clear_user_context(self, user_id: str):
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
    
    def get_memory_context(self, user_id: str, group_id: str, system_prompt: str = "", bot_name: str = "") -> list:
        return self.memory_manager.get_context_for_ai(user_id, group_id, system_prompt, bot_name)
    
    def add_to_memory(self, user_id: str, group_id: str, user_name: str, content: str, role: str = "user"):
        return self.memory_manager.add_message(user_id, group_id, user_name, content, role)
    
    def clear_memory(self, user_id: str, group_id: str):
        self.memory_manager.clear_memory(user_id, group_id)
    
    def set_memory_mode(self, user_id: str, mode: MemoryMode):
        self.memory_manager.set_user_memory_mode(user_id, mode)
    
    def get_memory_mode(self, user_id: str) -> MemoryMode:
        return self.memory_manager.get_user_memory_mode(user_id)
    
    def get_memory_status(self, user_id: str, group_id: str) -> Dict[str, Any]:
        return self.memory_manager.get_memory_status(user_id, group_id)
    
    # 全局预设管理方法
    def set_global_preset(self, group_id: str, preset_name: str):
        self.memory_manager.set_global_preset(group_id, preset_name)
    
    def get_global_preset(self, group_id: str) -> Optional[str]:
        return self.memory_manager.get_global_preset(group_id)
    
    def clear_global_preset(self, group_id: str):
        self.memory_manager.clear_global_preset(group_id)
    
    def is_enabled(self) -> bool:
        return self.enabled
    
    def set_enabled(self, enabled: bool):
        self.enabled = enabled
    
    def get_plugin_info(self) -> Dict[str, Any]:
        return {
            "name": self.plugin_name,
            "description": self.plugin_description,
            "version": self.plugin_version,
            "display_name": self.display_name,
            "trigger_keywords": self.trigger_keywords,
            "supports_images": self.supports_images,
            "supports_streaming": self.supports_streaming,
            "enabled": self.enabled
        }