"""
AI插件管理器
负责加载、管理和调用AI插件
"""
import os
import sys
import json
import uuid
import importlib.util
import traceback
from typing import Dict, List, Optional, Any
from .base_ai_plugin import BaseAIPlugin


class AIPluginManager:
    """AI插件管理器"""
    
    def __init__(self, plugins_dir: str = "ai_plugins", config_file: str = "config/ai_plugins_config.json"):
        """
        初始化AI插件管理器
        
        Args:
            plugins_dir: AI插件目录
            config_file: 配置文件路径
        """
        self.plugins_dir = plugins_dir
        self.config_file = config_file
        self.plugins: Dict[str, BaseAIPlugin] = {}
        self.plugin_configs: Dict[str, Dict] = {}
        self.current_plugin: Optional[str] = None
        
        # 确保目录存在
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
            
        # 加载配置
        self.load_config()
        
        # 加载插件
        self.load_plugins()
    
    def load_config(self):
        """加载插件配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.plugin_configs = config.get('plugins', {})
                    self.current_plugin = config.get('current_plugin', None)
            else:
                # 创建默认配置
                self.create_default_config()
        except Exception as e:
            print(f"加载AI插件配置失败: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置"""
        default_config = {
            "current_plugin": None,
            "plugins": {}
        }
        
        # 确保配置目录存在
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"创建默认AI插件配置失败: {e}")
    
    def save_config(self):
        """保存插件配置"""
        try:
            config = {
                "current_plugin": self.current_plugin,
                "plugins": self.plugin_configs
            }
            
            # 确保配置目录存在
            config_dir = os.path.dirname(self.config_file)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
                
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存AI插件配置失败: {e}")
    
    def load_plugins(self):
        """加载所有AI插件"""
        self.plugins.clear()
        
        if not os.path.exists(self.plugins_dir):
            print(f"AI插件目录不存在: {self.plugins_dir}")
            return
        
        for filename in os.listdir(self.plugins_dir):
            if filename.startswith('__') or filename.startswith('.'):
                continue
                
            plugin_path = os.path.join(self.plugins_dir, filename)
            
            # 处理目录形式的插件
            if os.path.isdir(plugin_path):
                plugin_file = os.path.join(plugin_path, f"{filename}_plugin.py")
                if os.path.exists(plugin_file):
                    self.load_plugin_file(plugin_file, filename)
            
            # 处理文件形式的插件
            elif filename.endswith('_plugin.py'):
                plugin_name = filename[:-10]  # 移除 '_plugin.py'
                self.load_plugin_file(plugin_path, plugin_name)
    
    def load_plugin_file(self, plugin_file: str, plugin_name: str):
        """加载单个插件文件"""
        try:
            # 生成唯一模块名
            unique_module_name = f"ai_plugin_{plugin_name}_{uuid.uuid4().hex[:8]}"
            
            # 确保AI插件目录在sys.path中
            ai_plugins_dir = os.path.dirname(plugin_file)
            if ai_plugins_dir not in sys.path:
                sys.path.insert(0, ai_plugins_dir)
            
            # 创建模块规范
            spec = importlib.util.spec_from_file_location(unique_module_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[unique_module_name] = module
            spec.loader.exec_module(module)
            
            # 查找插件类
            plugin_class = None
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (isinstance(item, type) and 
                    hasattr(item, '__bases__') and
                    any(base.__name__ == 'BaseAIPlugin' for base in item.__mro__) and
                    item.__name__ != 'BaseAIPlugin'):
                    plugin_class = item
                    break
            
            if plugin_class:
                # 获取插件配置
                plugin_config = self.plugin_configs.get(plugin_name, {})
                
                # 创建插件实例
                plugin_instance = plugin_class(plugin_config)
                self.plugins[plugin_name] = plugin_instance
                
                print(f"已加载AI插件: {plugin_name} - {plugin_instance.display_name}")
                
                # 如果没有设置当前插件，设置为第一个加载的插件
                if self.current_plugin is None:
                    self.current_plugin = plugin_name
                    self.save_config()
                    
            else:
                print(f"在插件文件中未找到有效的插件类: {plugin_file}")
                
        except Exception as e:
            print(f"加载AI插件失败 {plugin_name}: {e}")
            traceback.print_exc()
    
    def get_plugin(self, plugin_name: str) -> Optional[BaseAIPlugin]:
        """获取指定插件"""
        return self.plugins.get(plugin_name)
    
    def get_current_plugin(self) -> Optional[BaseAIPlugin]:
        """获取当前激活的插件"""
        if self.current_plugin and self.current_plugin in self.plugins:
            plugin = self.plugins[self.current_plugin]
            if plugin.is_enabled():
                return plugin
        return None
    
    def set_current_plugin(self, plugin_name: str) -> bool:
        """设置当前激活的插件"""
        if plugin_name in self.plugins:
            self.current_plugin = plugin_name
            self.save_config()
            return True
        return False
    
    def get_plugin_by_keyword(self, keyword: str) -> Optional[BaseAIPlugin]:
        """根据关键词获取插件"""
        for plugin in self.plugins.values():
            if keyword in plugin.trigger_keywords and plugin.is_enabled():
                return plugin
        return None
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """列出所有插件信息"""
        return [plugin.get_plugin_info() for plugin in self.plugins.values()]
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].set_enabled(True)
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].set_enabled(False)
            return True
        return False
    
    def reload_plugins(self):
        """重新加载所有插件"""
        print("重新加载AI插件...")
        
        # 清理模块
        modules_to_remove = []
        for module_name in sys.modules:
            if module_name.startswith('ai_plugin_'):
                modules_to_remove.append(module_name)
        
        for module_name in modules_to_remove:
            del sys.modules[module_name]
        
        # 重新加载
        self.load_plugins()
        print(f"AI插件重新加载完成，共加载 {len(self.plugins)} 个插件")
    
    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """获取插件配置"""
        return self.plugin_configs.get(plugin_name, {})
    
    def update_plugin_config(self, plugin_name: str, config: Dict[str, Any]):
        """更新插件配置"""
        self.plugin_configs[plugin_name] = config
        self.save_config()
        
        # 如果插件已加载，重新初始化
        if plugin_name in self.plugins:
            plugin_class = type(self.plugins[plugin_name])
            self.plugins[plugin_name] = plugin_class(config)