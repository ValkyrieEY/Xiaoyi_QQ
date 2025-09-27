# -*- coding: utf-8 -*-

"""
群组通知管理器
负责管理每个群的入群和退群提示开关
"""

import json
import os
from typing import Dict, Any, Optional


class GroupNoticeManager:
    """群组通知管理器"""
    
    def __init__(self, config_dir: str = "data"):
        self.config_dir = config_dir
        self.notice_dir = os.path.join(config_dir, "group_notice")
        
        # 确保目录存在
        os.makedirs(self.notice_dir, exist_ok=True)
        
        # 默认配置
        self.default_config = {
            "welcome_enabled": True,      # 入群欢迎开关
            "farewell_enabled": True,     # 退群提示开关
            "welcome_message": "",        # 自定义入群消息（空则使用默认）
            "farewell_message": "",       # 自定义退群消息（空则使用默认）
            "created_at": "",
            "updated_at": ""
        }
    
    def get_config_path(self, group_id: int) -> str:
        """获取群组配置文件路径"""
        return os.path.join(self.notice_dir, f"{group_id}.json")
    
    def load_group_config(self, group_id: int) -> Dict[str, Any]:
        """加载群组配置"""
        config_path = self.get_config_path(group_id)
        
        if not os.path.exists(config_path):
            # 如果配置文件不存在，创建默认配置
            config = self.default_config.copy()
            from datetime import datetime
            config["created_at"] = datetime.now().isoformat()
            config["updated_at"] = datetime.now().isoformat()
            self.save_group_config(group_id, config)
            return config
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 确保所有必要的键都存在
            for key, default_value in self.default_config.items():
                if key not in config:
                    config[key] = default_value
            
            return config
            
        except Exception as e:
            print(f"加载群组 {group_id} 配置失败: {e}")
            return self.default_config.copy()
    
    def save_group_config(self, group_id: int, config: Dict[str, Any]) -> bool:
        """保存群组配置"""
        try:
            from datetime import datetime
            config["updated_at"] = datetime.now().isoformat()
            
            config_path = self.get_config_path(group_id)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            print(f"群组 {group_id} 配置已保存")
            return True
            
        except Exception as e:
            print(f"保存群组 {group_id} 配置失败: {e}")
            return False
    
    def is_welcome_enabled(self, group_id: int) -> bool:
        """检查群组是否启用入群欢迎"""
        config = self.load_group_config(group_id)
        return config.get("welcome_enabled", True)
    
    def is_farewell_enabled(self, group_id: int) -> bool:
        """检查群组是否启用退群提示"""
        config = self.load_group_config(group_id)
        return config.get("farewell_enabled", True)
    
    def set_welcome_enabled(self, group_id: int, enabled: bool) -> bool:
        """设置群组入群欢迎开关"""
        config = self.load_group_config(group_id)
        config["welcome_enabled"] = enabled
        return self.save_group_config(group_id, config)
    
    def set_farewell_enabled(self, group_id: int, enabled: bool) -> bool:
        """设置群组退群提示开关"""
        config = self.load_group_config(group_id)
        config["farewell_enabled"] = enabled
        return self.save_group_config(group_id, config)
    
    def get_welcome_message(self, group_id: int) -> Optional[str]:
        """获取群组自定义入群消息"""
        config = self.load_group_config(group_id)
        message = config.get("welcome_message", "").strip()
        return message if message else None
    
    def get_farewell_message(self, group_id: int) -> Optional[str]:
        """获取群组自定义退群消息"""
        config = self.load_group_config(group_id)
        message = config.get("farewell_message", "").strip()
        return message if message else None
    
    def set_welcome_message(self, group_id: int, message: str) -> bool:
        """设置群组自定义入群消息"""
        config = self.load_group_config(group_id)
        config["welcome_message"] = message.strip()
        return self.save_group_config(group_id, config)
    
    def set_farewell_message(self, group_id: int, message: str) -> bool:
        """设置群组自定义退群消息"""
        config = self.load_group_config(group_id)
        config["farewell_message"] = message.strip()
        return self.save_group_config(group_id, config)
    
    def get_group_status(self, group_id: int) -> Dict[str, Any]:
        """获取群组通知状态"""
        config = self.load_group_config(group_id)
        return {
            "group_id": group_id,
            "welcome_enabled": config.get("welcome_enabled", True),
            "farewell_enabled": config.get("farewell_enabled", True),
            "has_custom_welcome": bool(config.get("welcome_message", "").strip()),
            "has_custom_farewell": bool(config.get("farewell_message", "").strip()),
            "created_at": config.get("created_at", ""),
            "updated_at": config.get("updated_at", "")
        }
    
    def list_all_groups(self) -> list:
        """列出所有有配置的群组"""
        try:
            groups = []
            for filename in os.listdir(self.notice_dir):
                if filename.endswith('.json'):
                    try:
                        group_id = int(filename[:-5])  # 去除.json后缀
                        status = self.get_group_status(group_id)
                        groups.append(status)
                    except ValueError:
                        continue
            
            return sorted(groups, key=lambda x: x['group_id'])
            
        except Exception as e:
            print(f"列出群组配置失败: {e}")
            return []
    
    def delete_group_config(self, group_id: int) -> bool:
        """删除群组配置"""
        try:
            config_path = self.get_config_path(group_id)
            if os.path.exists(config_path):
                os.remove(config_path)
                print(f"群组 {group_id} 配置已删除")
                return True
            return False
            
        except Exception as e:
            print(f"删除群组 {group_id} 配置失败: {e}")
            return False