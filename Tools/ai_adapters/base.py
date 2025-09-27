from abc import ABC, abstractmethod
from typing import Any, Dict, AsyncGenerator, Optional, Union
from dataclasses import dataclass
from enum import Enum

class MemoryScope(Enum):
    GLOBAL = "global"  # 全局记忆
    USER = "user"      # 用户级别记忆
    GROUP = "group"    # 群组级别记忆

@dataclass
class Message:
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class BaseAIAdapter(ABC):
    
    def __init__(self, config: Dict[str, Any]):

        self.config = config
        self.memory_scope = MemoryScope.USER  # 默认使用用户级别记忆
        
    @abstractmethod
    async def generate_response(
        self,
        messages: list[Message],
        stream: bool = True,
        **kwargs
    ) -> AsyncGenerator[Union[str, Dict[str, Any]], None]:

        pass
    
    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:

        pass
    
    def set_memory_scope(self, scope: MemoryScope):
        """
        设置记忆范围
        
        Args:
            scope: 记忆范围枚举值
        """
        self.memory_scope = scope
    
    @abstractmethod
    async def clear_memory(self, context_id: str):
        """
        清除指定上下文的记忆
        
        Args:
            context_id: 上下文ID
        """
        pass 