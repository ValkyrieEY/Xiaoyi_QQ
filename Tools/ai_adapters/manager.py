from typing import Dict, Any, Optional
from .factory import AIAdapterFactory
from .config import AIAdapterConfig
from .base import Message, MemoryScope
import json

class AIAdapterManager:
    """Manager for AI adapters."""
    
    def __init__(self, config_path: str = "./config/ai_adapters.json"):
        """
        初始化AI适配器管理器
        
        Args:
            config_path: 配置文件路径
        """
        print(f"Initializing AIAdapterManager with config: {config_path}")
        self.config = AIAdapterConfig(config_path)
        self._adapters: Dict[str, Any] = {}
        self._current_adapter: Optional[str] = None
        self._init_adapters()
    
    def _init_adapters(self):
        """Initialize all configured adapters."""
        try:
            # 获取所有可用的适配器
            available_adapters = self.config.get_available_adapters()
            print(f"Available adapters from config: {available_adapters}")
            
            if not available_adapters:
                print("Warning: No adapters configured")
                return
                
            # 初始化每个适配器
            for name in available_adapters:
                print(f"\nInitializing adapter: {name}")
                adapter_config = self.config.get_adapter_config(name)
                print(f"Adapter config: {adapter_config}")
                
                if not adapter_config:
                    print(f"Warning: No configuration found for adapter {name}")
                    continue
                    
                if not adapter_config.get("api_key"):
                    print(f"Warning: No API key configured for adapter {name}")
                    continue
                    
                try:
                    print(f"Creating adapter {name} with config: {adapter_config}")
                    adapter = AIAdapterFactory.create_adapter(name, **adapter_config)
                    if adapter:
                        self._adapters[name] = adapter
                        print(f"Successfully initialized adapter: {name}")
                    else:
                        print(f"Failed to create adapter: {name}")
                except Exception as e:
                    print(f"Error initializing adapter {name}: {str(e)}")
                    
            # 设置默认适配器
            default_adapter = self.config.get_default_adapter()
            print(f"\nDefault adapter from config: {default_adapter}")
            
            if default_adapter in self._adapters:
                self._current_adapter = default_adapter
                print(f"Using default adapter: {default_adapter}")
            elif self._adapters:
                self._current_adapter = next(iter(self._adapters))
                print(f"No valid default adapter found, using: {self._current_adapter}")
            else:
                print("Warning: No adapters available")
                
            print(f"\nFinal state:")
            print(f"Available adapters: {list(self._adapters.keys())}")
            print(f"Current adapter: {self._current_adapter}")
                
        except Exception as e:
            print(f"Error during adapter initialization: {str(e)}")
            self._adapters = {}
            self._current_adapter = None
    
    def get_adapter(self, name: Optional[str] = None) -> Any:
        """Get an adapter instance by name."""
        if name is None:
            name = self._current_adapter
            
        if not name:
            raise ValueError("No adapter available")
            
        if name not in self._adapters:
            raise ValueError(f"Adapter {name} not found")
            
        return self._adapters[name]
    
    def set_adapter(self, name: str):
        """Switch to a different adapter."""
        if name not in self._adapters:
            raise ValueError(f"Adapter {name} not found")
            
        self._current_adapter = name
        print(f"Switched to {name} adapter")
    
    def get_current_adapter(self) -> str:
        """Get the name of the current adapter."""
        return self._current_adapter or "No adapter available"
    
    def set_memory_scope(self, scope: MemoryScope, adapter_name: Optional[str] = None):
        """Set memory scope for an adapter."""
        adapter = self.get_adapter(adapter_name)
        adapter.memory_scope = scope
    
    async def clear_memory(self, context_id: str, adapter_name: Optional[str] = None):
        """Clear memory for an adapter."""
        adapter = self.get_adapter(adapter_name)
        await adapter.clear_memory(context_id)
    
    def get_available_adapters(self) -> list[str]:
        """Get list of available adapter names."""
        return list(self._adapters.keys())
    
    def reload_config(self):
        """Reload configuration and reinitialize adapters."""
        print("Reloading configuration...")
        self.config._load_config()
        self._adapters.clear()
        self._init_adapters() 