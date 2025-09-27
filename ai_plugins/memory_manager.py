"""
AI插件记忆管理器
"""
import json
import os
from typing import Dict, List, Any, Optional
from enum import Enum
import datetime


class MemoryMode(Enum):
    """记忆模式枚举"""
    GLOBAL = "global"  # 全局记忆（群组共享）
    PERSONAL = "personal"  # 个人记忆（用户独享）


class MessageInfo:
    """消息信息类"""
    def __init__(self, user_id: str, user_name: str, content: str, timestamp: str, role: str = "user"):
        self.user_id = user_id
        self.user_name = user_name
        self.content = content
        self.timestamp = timestamp
        self.role = role
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "content": self.content,
            "timestamp": self.timestamp,
            "role": self.role
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageInfo':
        return cls(
            user_id=data.get("user_id", ""),
            user_name=data.get("user_name", ""),
            content=data.get("content", ""),
            timestamp=data.get("timestamp", ""),
            role=data.get("role", "user")
        )


class AIMemoryManager:
    """AI记忆管理器"""
    
    def __init__(self, memory_dir: str = "data/ai_memory"):
        self.memory_dir = memory_dir
        self.user_memory_modes: Dict[str, MemoryMode] = {}  # 用户记忆模式设置
        self.memory_cache: Dict[str, List[MessageInfo]] = {}  # 记忆缓存
        self.max_context_length = 50  # 最大上下文长度
        self.global_presets: Dict[str, str] = {}  # 群组全局预设设置 {group_id: preset_name}
        
        # 确保目录存在
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
        
        # 加载用户记忆模式设置
        self.load_memory_modes()
        # 加载全局预设设置
        self.load_global_presets()
    
    def get_memory_file_path(self, context_id: str) -> str:
        """获取记忆文件路径"""
        return os.path.join(self.memory_dir, f"{context_id}.json")
    
    def get_global_presets_file_path(self) -> str:
        """获取全局预设配置文件路径"""
        return os.path.join(self.memory_dir, "global_presets.json")
    
    def get_memory_modes_file_path(self) -> str:
        """获取记忆模式配置文件路径"""
        return os.path.join(self.memory_dir, "memory_modes.json")
    
    def load_global_presets(self):
        """加载群组全局预设设置"""
        try:
            presets_file = self.get_global_presets_file_path()
            if os.path.exists(presets_file):
                with open(presets_file, 'r', encoding='utf-8') as f:
                    self.global_presets = json.load(f)
        except Exception as e:
            print(f"加载全局预设设置失败: {e}")
    
    def save_global_presets(self):
        """保存群组全局预设设置"""
        try:
            presets_file = self.get_global_presets_file_path()
            with open(presets_file, 'w', encoding='utf-8') as f:
                json.dump(self.global_presets, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存全局预设设置失败: {e}")
    
    def set_global_preset(self, group_id: str, preset_name: str):
        """设置群组全局预设"""
        self.global_presets[group_id] = preset_name
        self.save_global_presets()
    
    def get_global_preset(self, group_id: str) -> Optional[str]:
        """获取群组全局预设"""
        return self.global_presets.get(group_id)
    
    def clear_global_preset(self, group_id: str):
        """清除群组全局预设"""
        if group_id in self.global_presets:
            del self.global_presets[group_id]
            self.save_global_presets()
    
    def load_memory_modes(self):
        """加载用户记忆模式设置"""
        try:
            modes_file = self.get_memory_modes_file_path()
            if os.path.exists(modes_file):
                with open(modes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for user_id, mode_str in data.items():
                        self.user_memory_modes[user_id] = MemoryMode(mode_str)
        except Exception as e:
            print(f"加载记忆模式设置失败: {e}")
    
    def save_memory_modes(self):
        """保存用户记忆模式设置"""
        try:
            modes_file = self.get_memory_modes_file_path()
            data = {user_id: mode.value for user_id, mode in self.user_memory_modes.items()}
            with open(modes_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存记忆模式设置失败: {e}")
    
    def get_user_memory_mode(self, user_id: str) -> MemoryMode:
        """获取用户的记忆模式"""
        return self.user_memory_modes.get(user_id, MemoryMode.GLOBAL)
    
    def set_user_memory_mode(self, user_id: str, mode: MemoryMode):
        """设置用户的记忆模式"""
        self.user_memory_modes[user_id] = mode
        self.save_memory_modes()
    
    def get_context_id(self, user_id: str, group_id: str) -> str:
        """根据用户记忆模式获取上下文ID"""
        mode = self.get_user_memory_mode(user_id)
        if mode == MemoryMode.GLOBAL:
            return f"group_{group_id}"
        else:  # PERSONAL
            return f"user_{user_id}_in_group_{group_id}"
    
    def load_memory(self, context_id: str) -> List[MessageInfo]:
        """加载记忆"""
        if context_id in self.memory_cache:
            return self.memory_cache[context_id]
        
        try:
            memory_file = self.get_memory_file_path(context_id)
            if os.path.exists(memory_file):
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    messages = [MessageInfo.from_dict(msg_data) for msg_data in data]
                    self.memory_cache[context_id] = messages
                    return messages
        except Exception as e:
            print(f"加载记忆失败 {context_id}: {e}")
        
        return []
    
    def save_memory(self, context_id: str, messages: List[MessageInfo]):
        """保存记忆"""
        try:
            memory_file = self.get_memory_file_path(context_id)
            data = [msg.to_dict() for msg in messages]
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 更新缓存
            self.memory_cache[context_id] = messages
        except Exception as e:
            print(f"保存记忆失败 {context_id}: {e}")
    
    def add_message(self, user_id: str, group_id: str, user_name: str, content: str, role: str = "user"):
        """添加消息到记忆"""
        context_id = self.get_context_id(user_id, group_id)
        messages = self.load_memory(context_id)
        
        # 创建消息信息
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_info = MessageInfo(user_id, user_name, content, timestamp, role)
        
        # 添加到记忆
        messages.append(message_info)
        
        # 限制记忆长度
        if len(messages) > self.max_context_length:
            # 保留系统消息和最近的对话
            system_messages = [msg for msg in messages if msg.role == "system"]
            recent_messages = [msg for msg in messages if msg.role != "system"][-self.max_context_length:]
            messages = system_messages + recent_messages
        
        # 保存记忆
        self.save_memory(context_id, messages)
        
        return context_id
    
    def get_context_for_ai(self, user_id: str, group_id: str, system_prompt: str = "", bot_name: str = "") -> List[Dict[str, str]]:
        """获取AI使用的上下文格式"""
        context_id = self.get_context_id(user_id, group_id)
        messages = self.load_memory(context_id)
        mode = self.get_user_memory_mode(user_id)  # 在开始就获取用户记忆模式
        
        # 构建AI格式的上下文
        ai_context = []
        
        # 添加系统消息
        if system_prompt:
            if mode == MemoryMode.GLOBAL:
                # 全局记忆模式下，检查是否有全局预设
                global_preset = self.get_global_preset(group_id)
                if global_preset:
                    # 使用全局预设，需要从预设系统加载
                    try:
                        import sys
                        import os
                        # 添加项目根目录到路径
                        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                        if project_root not in sys.path:
                            sys.path.insert(0, project_root)
                        import prerequisites.prerequisite as presets_tool
                        
                        # 读取全局预设内容
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
                                        
                                        enhanced_prompt = f"{global_system_prompt}\n\n注意：当前为群组全局记忆模式，请根据消息中的用户信息区分不同的发言者。用户信息格式为：[用户名(QQ:用户ID) 时间] 消息内容"
                                        ai_context.append({"role": "system", "content": enhanced_prompt})
                                        break
                                break
                        else:
                            # 如果找不到全局预设，使用默认系统提示
                            enhanced_prompt = f"{system_prompt}\n\n注意：当前为群组全局记忆模式，请根据消息中的用户信息区分不同的发言者。用户信息格式为：[用户名(QQ:用户ID) 时间] 消息内容"
                            ai_context.append({"role": "system", "content": enhanced_prompt})
                    except Exception as e:
                        print(f"加载全局预设失败: {e}")
                        # 如果加载失败，使用默认系统提示
                        enhanced_prompt = f"{system_prompt}\n\n注意：当前为群组全局记忆模式，请根据消息中的用户信息区分不同的发言者。用户信息格式为：[用户名(QQ:用户ID) 时间] 消息内容"
                        ai_context.append({"role": "system", "content": enhanced_prompt})
                else:
                    # 如果没有设置全局预设，使用默认系统提示
                    enhanced_prompt = f"{system_prompt}\n\n注意：当前为群组全局记忆模式，请根据消息中的用户信息区分不同的发言者。用户信息格式为：[用户名(QQ:用户ID) 时间] 消息内容"
                    ai_context.append({"role": "system", "content": enhanced_prompt})
            else:
                enhanced_prompt = f"{system_prompt}\n\n注意：当前为个人记忆模式，你正在与单个用户进行对话。"
                ai_context.append({"role": "system", "content": enhanced_prompt})
        
        # 添加历史消息
        for msg in messages:
            if msg.role == "system":
                continue  # 系统消息已经在上面添加
            elif msg.role == "user":
                # 格式化用户消息，包含发送者信息
                if mode == MemoryMode.GLOBAL:
                    formatted_content = f"[{msg.user_name}(QQ:{msg.user_id}) {msg.timestamp}] {msg.content}"
                else:
                    formatted_content = msg.content  # 个人记忆模式不需要格式化
                ai_context.append({"role": "user", "content": formatted_content})
            elif msg.role == "assistant":
                # AI回复不需要特殊格式化
                ai_context.append({"role": "assistant", "content": msg.content})
        
        return ai_context
    
    def clear_memory(self, user_id: str, group_id: str):
        """清除记忆"""
        context_id = self.get_context_id(user_id, group_id)
        
        # 清除文件
        memory_file = self.get_memory_file_path(context_id)
        if os.path.exists(memory_file):
            os.remove(memory_file)
        
        # 清除缓存
        if context_id in self.memory_cache:
            del self.memory_cache[context_id]
    
    def get_memory_status(self, user_id: str, group_id: str) -> Dict[str, Any]:
        """获取记忆状态信息"""
        mode = self.get_user_memory_mode(user_id)
        context_id = self.get_context_id(user_id, group_id)
        messages = self.load_memory(context_id)
        
        return {
            "mode": mode.value,
            "context_id": context_id,
            "message_count": len(messages),
            "mode_description": "群组全局记忆" if mode == MemoryMode.GLOBAL else "个人独立记忆"
        }