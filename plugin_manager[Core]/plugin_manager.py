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

__name__ = "plugin_manager"
__version__ = "1.1.0"
__author__ = "Xiaoyi"

PLUGIN_FOLDER = "plugins"
MENU_FILE = "plugin_menu.json"
START_TIME = time.time()
LAST_SHUTDOWN_FILE = "last_shutdown.txt"
LOG_FILE = "bot.log"
HISTORY_FILE = "message_history.json"

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

# 在消息处理函数中记录消息
async def on_message(event, actions):
    message = str(event.message).strip()
    log_message({"user_id": event.user_id, "group_id": event.group_id, "message": message, "timestamp": time.time()})
    
    if message == "启动插件管理器WebUI":
        threading.Thread(target=start_webui, daemon=True).start()
        return "插件管理器WebUI已启动，请访问 http://localhost:36674"
    
    if message.startswith("添加菜单 "):
        item = message[5:].strip()
        menu = load_menu()
        if item not in menu:
            menu.append(item)
            save_menu(menu)
            return f"已添加 '{item}' 到菜单。"
        else:
            return f"'{item}' 已在菜单中。"

    elif message.startswith("删除菜单 "):
        item = message[5:].strip()
        menu = load_menu()
        if item in menu:
            menu.remove(item)
            save_menu(menu)
            return f"已从菜单中删除 '{item}'。"
        else:
            return f"'{item}' 不在菜单中。"

    elif message == "显示菜单":
        menu = load_menu()
        return "当前菜单：\n" + "\n".join(menu) if menu else "菜单为空。"

    elif message.startswith("启用插件 "):
        plugin_name = message[4:].strip()
        if toggle_plugin(plugin_name, True):
            return f"已启用插件 '{plugin_name}'。"
        else:
            return f"无法启用插件 '{plugin_name}'，可能不存在或已启用。"

    elif message.startswith("停用插件 "):
        plugin_name = message[4:].strip()
        if toggle_plugin(plugin_name, False):
            return f"已停用插件 '{plugin_name}'。"
        else:
            return f"无法停用插件 '{plugin_name}'，可能不存在或已停用。"

    elif message.startswith("插件信息 "):
        plugin_name = message[4:].strip()
        info = get_plugin_info(plugin_name)
        if "error" in info:
            return f"获取插件 '{plugin_name}' 信息失败：{info['error']}"
        else:
            return f"插件 '{plugin_name}' 信息：\n名称：{info['name']}\n版本：{info['version']}\n作者：{info['author']}"

    elif message == "列出插件":
        plugins = [f.replace('.py', '') for f in os.listdir(PLUGIN_FOLDER) if f.endswith('.py')]
        return "已安装的插件：\n" + "\n".join(plugins)

    return None

# 插件元数据
__name__ = "插件管理器"
__version__ = "1.0"
__author__ = "Xiaoyi"