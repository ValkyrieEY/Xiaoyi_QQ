from typing import Dict, Any, List
import json
import os

class AIAdapterConfig:
    """AI适配器配置管理"""
    
    def __init__(self, config_path: str = "./config/ai_adapters.json"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            # 创建默认配置
            self.config = {
                "default_adapter": "gemini",
                "adapters": {
                    "gemini": {
                        "api_key": "",
                        "model": "gemini-pro",
                        "memory_path": "./data/memory"
                    },
                    "deepseek": {
                        "api_key": "",
                        "model": "deepseek-chat",
                        "memory_path": "./data/memory"
                    }
                },
                "memory": {
                    "scope": "conversation",
                    "max_tokens": 1000
                }
            }
            self._save_config()
    
    def _save_config(self):
        """保存配置到文件"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_adapter_config(self, adapter_name: str) -> Dict[str, Any]:
        """
        获取指定适配器的配置
        
        Args:
            adapter_name: 适配器名称
            
        Returns:
            适配器配置字典
        """
        return self.config["adapters"].get(adapter_name, {})
    
    def set_adapter_config(self, adapter_name: str, config: Dict[str, Any]):
        """
        设置适配器配置
        
        Args:
            adapter_name: 适配器名称
            config: 配置字典
        """
        self.config["adapters"][adapter_name] = config
        self._save_config()
    
    def get_default_adapter(self) -> str:
        """
        获取默认适配器名称
        
        Returns:
            默认适配器名称
        """
        return self.config["default_adapter"]
    
    def set_default_adapter(self, adapter_name: str):
        """
        设置默认适配器
        
        Args:
            adapter_name: 适配器名称
        """
        self.config["default_adapter"] = adapter_name
        self._save_config()
        
    def get_available_adapters(self) -> List[str]:
        """
        获取所有可用的适配器名称
        
        Returns:
            适配器名称列表
        """
        return list(self.config["adapters"].keys())
        
    def get_memory_config(self) -> Dict[str, Any]:
        """
        获取内存配置
        
        Returns:
            内存配置字典
        """
        return self.config.get("memory", {
            "scope": "conversation",
            "max_tokens": 1000
        }) 