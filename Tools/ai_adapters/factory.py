from typing import Dict, Type, Optional
from .base import BaseAIAdapter
from .gemini_adapter import GeminiAdapter
from .deepseek_adapter import DeepseekAdapter

class AIAdapterFactory:
    """Factory for creating AI adapters."""
    
    _adapters: Dict[str, Type[BaseAIAdapter]] = {
        "gemini": GeminiAdapter,
        "deepseek": DeepseekAdapter
    }
    
    @classmethod
    def register_adapter(cls, name: str, adapter_class: Type[BaseAIAdapter]):
        """Register a new adapter."""
        print(f"Registering adapter: {name}")
        cls._adapters[name] = adapter_class
        
    @classmethod
    def create_adapter(cls, name: str, **kwargs) -> Optional[BaseAIAdapter]:
        """Create an adapter instance."""
        print(f"Creating adapter: {name}")
        print(f"Available adapters: {list(cls._adapters.keys())}")
        
        adapter_class = cls._adapters.get(name)
        if adapter_class:
            print(f"Found adapter class: {adapter_class.__name__}")
            try:
                adapter = adapter_class(**kwargs)
                print(f"Successfully created adapter instance")
                return adapter
            except Exception as e:
                print(f"Error creating adapter instance: {str(e)}")
                return None
        else:
            print(f"Adapter class not found for: {name}")
            return None
        
    @classmethod
    def get_available_adapters(cls) -> list[str]:
        """Get list of available adapter names."""
        return list(cls._adapters.keys()) 