import os
import json
import psutil
import platform
import time
import datetime
import importlib.util
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import threading
import subprocess
from Hyper import Configurator, Manager, Segments

# 插件元数据
TRIGGHT_KEYWORD = "plugin"  # 插件管理相关命令触发
HELP_MESSAGE = """插件管理器
普通用户指令：
plugin list - 列出所有插件
plugin info <插件名> - 查看插件信息

管理员指令：
plugin ui - 启动插件管理器WebUI（需要管理员权限）
plugin enable <插件名> - 启用插件（需要管理员权限）
plugin disable <插件名> - 停用插件（需要管理员权限）
plugin menu add <项目> - 添加菜单项（需要管理员权限）
plugin menu remove <项目> - 删除菜单项（需要管理员权限）
plugin menu show - 显示菜单（需要管理员权限）"""

__name__ = "PluginManager"
__version__ = "1.1.0"
__author__ = "Xiaoyi"

PLUGIN_FOLDER = "plugins"
MENU_FILE = "plugin_menu.json"
START_TIME = time.time()
LAST_SHUTDOWN_FILE = "last_shutdown.txt"
LOG_FILE = "bot.log"
HISTORY_FILE = "message_history.json"

# 在文件开头添加路径常量
MANAGE_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Manage_User.ini")
SUPER_USER_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Super_User.ini")

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 用于加密会话数据

# 默认管理员账号
DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWORD = 'admin'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='用户名或密码错误')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.before_request
def require_login():
    if not session.get('logged_in') and request.endpoint not in ['login', 'static']:
        return redirect(url_for('login'))

def get_system_info():
    """获取系统信息"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # 计算运行时间
    uptime = time.time() - START_TIME
    uptime_str = str(datetime.timedelta(seconds=int(uptime)))
    
    # 获取上次关闭时间
    last_shutdown = "未知"
    if os.path.exists(LAST_SHUTDOWN_FILE):
        with open(LAST_SHUTDOWN_FILE, 'r') as f:
            try:
                last_shutdown = f.read().strip()
            except:
                pass

    return {
        "os": platform.system() + " " + platform.release(),
        "cpu_percent": cpu_percent,
        "memory_total": bytes_to_human(memory.total),
        "memory_used": bytes_to_human(memory.used),
        "memory_percent": memory.percent,
        "disk_total": bytes_to_human(disk.total),
        "disk_used": bytes_to_human(disk.used),
        "disk_percent": disk.percent,
        "uptime": uptime_str,
        "last_shutdown": last_shutdown,
        "python_version": platform.python_version(),
        "boot_time": datetime.datetime.fromtimestamp(
            psutil.boot_time()
        ).strftime("%Y-%m-%d %H:%M:%S")
    }

def bytes_to_human(bytes_val):
    """将字节转换为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"

# 添加新路由用于获取实时系统信息
@app.route('/system_info')  
def system_info():
    return jsonify(get_system_info())

@app.route('/')
def index():
    menu = load_menu()
    plugins = [f.replace('.py', '') for f in os.listdir(PLUGIN_FOLDER) if f.endswith('.py')]
    system_info = get_system_info()  # 获取系统信息
    return render_template('index.html', menu=menu, plugins=plugins, system_info=system_info)

@app.route('/logs')
def view_logs():
    with open(LOG_FILE, 'r') as f:
        logs = f.read()
    return render_template('logs.html', logs=logs)

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        group_id = request.form['group_id']
        message = request.form['message']
        # 发送消息的逻辑
        # ...
        return redirect(url_for('send_message'))
    return render_template('send_message.html')

@app.route('/history')
def view_history():
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
    return render_template('history.html', history=history)

@app.route('/delete_history', methods=['POST'])
def delete_history():
    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)
    return redirect(url_for('view_history'))

# 在程序退出时保存关闭时间
def save_shutdown_time():
    shutdown_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LAST_SHUTDOWN_FILE, 'w') as f:
        f.write(shutdown_time)

# 注册退出处理函数
import atexit
atexit.register(save_shutdown_time)

def load_menu():
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'r') as f:
            return json.load(f)
    return []

def save_menu(menu):
    with open(MENU_FILE, 'w') as f:
        json.dump(menu, f)

def get_plugin_info(plugin_name):
    try:
        spec = importlib.util.spec_from_file_location(plugin_name, os.path.join(PLUGIN_FOLDER, f"{plugin_name}.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return {
            "name": getattr(module, "__name__", "Unknown"),
            "version": getattr(module, "__version__", "Unknown"),
            "author": getattr(module, "__author__", "Unknown")
        }
    except Exception as e:
        return {"error": str(e)}

def toggle_plugin(plugin_name, enable=True):
    old_name = f"{'xyi_' if not enable else ''}{plugin_name}.py"
    new_name = f"{'xyi_' if enable else ''}{plugin_name}.py"
    old_path = os.path.join(PLUGIN_FOLDER, old_name)
    new_path = os.path.join(PLUGIN_FOLDER, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return True
    return False

@app.route('/add_menu', methods=['POST'])
def add_menu():
    item = request.form['item']
    menu = load_menu()
    if item not in menu:
        menu.append(item)
        save_menu(menu)
    return redirect(url_for('index'))

@app.route('/remove_menu', methods=['POST'])
def remove_menu():
    item = request.form['item']
    menu = load_menu()
    if item in menu:
        menu.remove(item)
        save_menu(menu)
    return redirect(url_for('index'))

@app.route('/toggle_plugin', methods=['POST'])
def toggle_plugin_route():
    plugin_name = request.form['plugin']
    action = request.form['action']
    toggle_plugin(plugin_name, action == 'enable')
    return redirect(url_for('index'))

@app.route('/plugin_info/<plugin_name>')
def plugin_info(plugin_name):
    info = get_plugin_info(plugin_name)
    return render_template('plugin_info.html', plugin_name=plugin_name, info=info)

@app.route('/restart', methods=['POST'])
def restart():
    if session.get('logged_in'):
        save_shutdown_time()
        os.system("shutdown -r -t 0")
        return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    if session.get('logged_in'):
        save_shutdown_time()
        os.system("shutdown -s -t 0")
        return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/execute_command', methods=['POST'])
def execute_command():
    if session.get('logged_in'):
        command = request.form['command']
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = e.stderr
        return render_template('command_result.html', command=command, output=output)
    return redirect(url_for('login'))

def start_webui():
    try:
        # 使用 127.0.0.1 而不是 localhost 以增加安全性
        # 添加 debug=False 以避免生产环境中的调试信息
        print("尝试启动 WebUI...")
        app.run(
            host='127.0.0.1',
            port=36674,
            debug=False,
            threaded=True  # 启用多线程支持
        )
    except Exception as e:
        print(f"WebUI 启动失败：{str(e)}")

# 在主线程中启动 WebUI
if __name__ == "__main__":
    threading.Thread(target=start_webui, daemon=True).start()

def log_message(message):
    with open(HISTORY_FILE, 'a') as f:
        json.dump(message, f)
        f.write('\n')

def read_user_groups():
    """读取管理员和超级用户组"""
    manage_users = []
    super_users = []
    
    # 读取 Manage_User.ini
    if os.path.exists(MANAGE_USER_INI):
        with open(MANAGE_USER_INI, 'r', encoding='utf-8') as f:
            manage_users = [line.strip() for line in f if line.strip()]
    
    # 读取 Super_User.ini
    if os.path.exists(SUPER_USER_INI):
        with open(SUPER_USER_INI, 'r', encoding='utf-8') as f:
            super_users = [line.strip() for line in f if line.strip()]
    
    return manage_users, super_users

def is_admin(user_id: str) -> bool:
    """检查用户是否有管理员权限"""
    try:
        manage_users, super_users = read_user_groups()
        return user_id in manage_users or user_id in super_users
    except Exception as e:
        print(f"[PluginManager] 读取用户组配置失败: {str(e)}")
        return False

# 在消息处理函数中记录消息
async def on_message(event, actions, Manager, Segments):
    user_id = str(event.user_id)
    message = str(event.message).strip()
    
    # 记录消息
    log_message({
        "user_id": event.user_id, 
        "group_id": event.group_id, 
        "message": message, 
        "timestamp": time.time()
    })
    
    if not message.startswith("plugin"):
        return False
    
    cmd = message[6:].strip()

    # 普通用户命令
    if cmd == "list":
        plugins = [f.replace('.py', '') for f in os.listdir(PLUGIN_FOLDER) if f.endswith('.py')]
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("已安装的插件：\n" + "\n".join(plugins)))
        )
        return True
    
    elif cmd.startswith("info "):
        plugin_name = cmd[5:].strip()
        info = get_plugin_info(plugin_name)
        if "error" in info:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"获取插件 '{plugin_name}' 信息失败：{info['error']}"))
            )
        else:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(
                    f"插件 '{plugin_name}' 信息：\n"
                    f"名称：{info['name']}\n"
                    f"版本：{info['version']}\n"
                    f"作者：{info['author']}"
                ))
            )
        return True

    # 管理员命令需要权限检查
    if not is_admin(user_id):
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("你没有权限执行此操作，此命令仅管理员可用。"))
        )
        return True

    # 以下是需要管理员权限的命令
    if cmd == "ui":
        threading.Thread(target=start_webui, daemon=True).start()
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("插件管理器WebUI已启动，请访问 http://localhost:36674"))
        )
        return True
    
    elif cmd.startswith("menu add "):
        item = cmd[9:].strip()
        menu = load_menu()
        if item not in menu:
            menu.append(item)
            save_menu(menu)
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"已添加 '{item}' 到菜单。"))
            )
        else:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"'{item}' 已在菜单中。"))
            )
        return True

    elif cmd.startswith("menu remove "):
        item = cmd[12:].strip()
        menu = load_menu()
        if item in menu:
            menu.remove(item)
            save_menu(menu)
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"已从菜单中删除 '{item}'。"))
            )
        else:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"'{item}' 不在菜单中。"))
            )
        return True

    elif cmd == "menu show":
        menu = load_menu()
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("当前菜单：\n" + "\n".join(menu) if menu else "菜单为空。"))
        )
        return True

    elif cmd.startswith("enable "):
        plugin_name = cmd[7:].strip()
        if toggle_plugin(plugin_name, True):
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"已启用插件 '{plugin_name}'。"))
            )
        else:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"无法启用插件 '{plugin_name}'，可能不存在或已启用。"))
            )
        return True

    elif cmd.startswith("disable "):
        plugin_name = cmd[8:].strip()
        if toggle_plugin(plugin_name, False):
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"已停用插件 '{plugin_name}'。"))
            )
        else:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"无法停用插件 '{plugin_name}'，可能不存在或已停用。"))
            )
        return True

    elif cmd.startswith("info "):
        plugin_name = cmd[5:].strip()
        info = get_plugin_info(plugin_name)
        if "error" in info:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"获取插件 '{plugin_name}' 信息失败：{info['error']}"))
            )
        else:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(
                    f"插件 '{plugin_name}' 信息：\n"
                    f"名称：{info['name']}\n"
                    f"版本：{info['version']}\n"
                    f"作者：{info['author']}"
                ))
            )
        return True

    elif cmd == "list":
        plugins = [f.replace('.py', '') for f in os.listdir(PLUGIN_FOLDER) if f.endswith('.py')]
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("已安装的插件：\n" + "\n".join(plugins)))
        )
        return True
    
    return False