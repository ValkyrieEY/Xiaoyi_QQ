import os
import importlib.util
from Hyper import Configurator, Manager, Segments, Events

# 插件元数据
TRIGGHT_KEYWORD = "Any"  # 需要处理所有消息以适配旧插件
HELP_MESSAGE = """旧版插件适配器
功能：加载和管理旧版本的插件
指令：
/plugin status - 查看已加载的旧版插件
/plugin reload - 重新加载旧版插件"""

__name__ = "OldPluginAdapter"
__version__ = "1.0.0"
__author__ = "Xiaoyi"

# 首先初始化配置管理器
if not hasattr(Configurator, 'cm'):
    Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

# 创建和检查旧插件目录
OLD_PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "old_plugins")
if not os.path.exists(OLD_PLUGIN_DIR):
    os.makedirs(OLD_PLUGIN_DIR)

# 存储加载的旧版插件
loaded_old_plugins = []

def load_old_plugins():
    """加载旧版插件"""
    global loaded_old_plugins
    loaded_old_plugins = []
    
    for root, dirs, files in os.walk(OLD_PLUGIN_DIR):
        for file in files:
            if (file.endswith('.py') or file.endswith('.pyw')) and not file.startswith('xyi_'):
                try:
                    module_name = os.path.splitext(file)[0]
                    module_path = os.path.join(root, file)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查插件必要属性
                    if not hasattr(module, 'on_message'):
                        print(f"警告: 插件 {module_name} 缺少 on_message 函数")
                        continue
                        
                    loaded_old_plugins.append(module)
                    print(f"✅ 成功加载旧版插件: {module_name}")
                except Exception as e:
                    print(f"❌ 加载旧版插件 {file} 失败: {str(e)}")
    
    return len(loaded_old_plugins)

# 初始加载插件
loaded_count = load_old_plugins()
print(f"已加载 {loaded_count} 个旧版插件")

async def on_message(event, actions, Manager, Segments):
    """处理消息事件"""
    user_message = str(event.message)
    
    # 处理插件管理命令
    if user_message.startswith("/plugin"):
        cmd = user_message[7:].strip()
        if cmd == "status":
            plugin_list = "\n".join([
                f"- {p.__name__} ({getattr(p, 'TRIGGHT_KEYWORD', 'Any')})"
                for p in loaded_old_plugins
            ])
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(
                    f"当前加载的旧版插件（{len(loaded_old_plugins)}个）：\n{plugin_list}"
                ))
            )
            return True
        elif cmd == "reload":
            count = load_old_plugins()
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"已重新加载 {count} 个旧版插件"))
            )
            return True
    
    # 处理旧版插件消息
    for plugin in loaded_old_plugins:
        try:
            # 检查触发条件
            if hasattr(plugin, 'TRIGGHT_KEYWORD'):
                if plugin.TRIGGHT_KEYWORD != "Any" and plugin.TRIGGHT_KEYWORD not in user_message:
                    continue
            
            # 调用插件处理函数
            result = await plugin.on_message(event, actions, Manager, Segments)
            if result is True:
                return True
        except Exception as e:
            print(f"执行旧版插件 {plugin.__name__} 时出错: {str(e)}")
    
    return False
