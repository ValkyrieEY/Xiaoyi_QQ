import json
import os
import requests
from flask import Flask, render_template, request, jsonify
import threading
import webbrowser
from Hyper import Configurator, Manager, Segments, Events

# 插件元数据
TRIGGHT_KEYWORD = "/api"
HELP_MESSAGE = """自定义API调用插件
指令：
/api config - 打开API配置界面
[其他已配置的API命令]"""

Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

__name__ = "CustomAPI"
__version__ = "1.0.0"
__author__ = "XiaoyiAPI"

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "custom_api_config.json")
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# 默认配置
DEFAULT_CONFIG = {
    "apis": [{
        "command": "天气",
        "url": "https://api.example.com/weather",
        "response_type": "text",
        "response_path": "weather.text",  # 指定要提取的JSON路径
        "params": [{
            "name": "city",         # API参数名
            "type": "user_input",   # 参数类型：user_input(用户输入), text(固定文本), sender_id(发送者ID)
            "value": ""            # 当type为text时使用的固定值
        }]
    }]
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config_data):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置失败: {str(e)}")
        return False

config = load_config()

@app.route('/')
def home():
    return render_template('custom_api.html', apis=config['apis'])

@app.route('/api/save', methods=['POST'])
def save_api():
    try:
        global config
        data = request.get_json()
        if data is None:
            return jsonify({"status": "error", "message": "无效的 JSON 数据"})
        
        config['apis'] = data
        if save_config(config):
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "配置保存失败"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def start_webui():
    try:
        app.run(port=4997, debug=False)
    except Exception as e:
        print(f"启动 WebUI 失败: {str(e)}")

async def on_message(event, actions, Manager, Segments):
    user_message = str(event.message)
    
    # 检查是否是管理命令
    if user_message == "/api config":
        threading.Thread(target=start_webui, daemon=True).start()
        webbrowser.open('http://localhost:4997')
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("已打开API配置界面，请在浏览器中操作")))
        return True
    
    # 处理API请求
    for api in config['apis']:
        if user_message.startswith(api['command']):
            try:
                # 获取命令参数
                user_input = user_message[len(api['command']):].strip()
                
                # 构建参数
                params = {}
                for param in api.get('params', []):
                    if param['type'] == 'user_input':
                        params[param['name']] = user_input
                    elif param['type'] == 'text':
                        params[param['name']] = param['value']
                    elif param['type'] == 'sender_id':
                        params[param['name']] = str(event.user_id)
                
                # 发送请求
                response = requests.get(api['url'], params=params)
                
                # 如果指定了响应路径，则提取指定字段
                if api.get('response_path'):
                    try:
                        result = response.json()
                        for key in api['response_path'].split('.'):
                            result = result.get(key, {})
                        response_text = str(result)
                    except:
                        response_text = response.text
                else:
                    response_text = response.text
                
                if api['response_type'] == 'image':
                    await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Image(response_text)))
                else:
                    await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(response_text)))
                return True
            except Exception as e:
                await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(f"API请求失败: {str(e)}")))
                return True
    
    return False