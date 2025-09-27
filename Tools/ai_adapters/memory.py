from typing import Dict, List, Optional
from .base import MemoryScope, Message
import json
import os
import glob

class MemoryManager:
    """记忆管理器，处理不同范围的记忆存储和检索"""
    
    def __init__(self, storage_path: str = "./data/memory"):
        """
        初始化记忆管理器
        
        Args:
            storage_path: 记忆存储路径
        """
        self.storage_path = storage_path
        self.memory: Dict[str, Dict[str, List[Message]]] = {
            MemoryScope.GLOBAL.value: {},
            MemoryScope.USER.value: {},
            MemoryScope.GROUP.value: {}
        }
        self._ensure_storage_path()
        self._load_memory()
    
    def _ensure_storage_path(self):
        """确保存储路径存在"""
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _get_memory_file_path(self, scope: MemoryScope, context_id: str) -> str:
        """获取记忆文件路径"""
        return os.path.join(self.storage_path, f"{scope.value}_{context_id}.json")
    
    def _load_memory(self):
        """加载所有记忆"""
        for scope in MemoryScope:
            scope_path = os.path.join(self.storage_path, f"{scope.value}_*")
            for file_path in glob.glob(scope_path):
                context_id = os.path.basename(file_path).split("_", 1)[1].replace(".json", "")
                with open(file_path, "r", encoding="utf-8") as f:
                    self.memory[scope.value][context_id] = [
                        Message(**msg) for msg in json.load(f)
                    ]
    
    def _save_memory(self, scope: MemoryScope, context_id: str):
        """保存指定范围的记忆"""
        file_path = self._get_memory_file_path(scope, context_id)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                [msg.__dict__ for msg in self.memory[scope.value][context_id]],
                f,
                ensure_ascii=False,
                indent=2
            )
    
    def add_message(self, scope: MemoryScope, context_id: str, message: Message):
        """
        添加消息到记忆
        
        Args:
            scope: 记忆范围
            context_id: 上下文ID
            message: 消息对象
        """
        if context_id not in self.memory[scope.value]:
            self.memory[scope.value][context_id] = []
        self.memory[scope.value][context_id].append(message)
        self._save_memory(scope, context_id)
    
    def get_messages(self, scope: MemoryScope, context_id: str) -> List[Message]:
        """
        获取指定范围的记忆
        
        Args:
            scope: 记忆范围
            context_id: 上下文ID
            
        Returns:
            消息列表
        """
        return self.memory[scope.value].get(context_id, [])
    
    def clear_memory(self, scope: MemoryScope, context_id: str):
        """
        清除指定范围的记忆
        
        Args:
            scope: 记忆范围
            context_id: 上下文ID
        """
        if context_id in self.memory[scope.value]:
            del self.memory[scope.value][context_id]
            file_path = self._get_memory_file_path(scope, context_id)
            if os.path.exists(file_path):
                os.remove(file_path)
    
    def get_combined_memory(self, context_id: str) -> List[Message]:
        """
        获取组合后的记忆（全局 + 用户/群组）
        
        Args:
            context_id: 上下文ID
            
        Returns:
            组合后的消息列表
        """
        messages = []
        # 添加全局记忆
        messages.extend(self.get_messages(MemoryScope.GLOBAL, "global"))
        # 添加用户/群组记忆
        messages.extend(self.get_messages(MemoryScope.USER, context_id))
        messages.extend(self.get_messages(MemoryScope.GROUP, context_id))
        return messages 