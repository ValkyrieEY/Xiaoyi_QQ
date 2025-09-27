from Hyper import Configurator
import json
import os
import re
import aiohttp
from datetime import datetime
import http.server
import socketserver
import threading
import webbrowser
import jinja2
import random
import uuid
import platform
import psutil
import asyncio

# 加载配置
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

TRIGGHT_KEYWORD = "Any"  # 使用Any让插件可以处理所有消息

SYSTEM_CONFIG = {
    "web_port": 8080,
    "auto_open_browser": False,
    "theme": "light",
    "admin_password": "",
    "log_api_calls": True
}

# API配置 - 增强版支持更多配置选项
DEFAULT_CONFIG = {
    "apis": [
        {
            "name": "示例API",
            "enabled": False,
            "use_prefix": True,
            "read_after_command": False,
            "trigger": "测试",
            "url": "https://example.com/api",
            "method": "GET",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Jianer-CustomAPI/1.0"
            },
            "body_template": {
                "message": "【用户消息】",
                "user_id": "【发送者QQ】",
                "group_id": "【群号】",
                "timestamp": "【时间戳】"
            },
            "response_template": "API返回: 【纯文本】\n发送者：【发送者昵称】\n时间：【当前时间】",
            "cooldown": 0,
            "timeout": 30,
            "max_retries": 3,
            "retry_delay": 1,
            "error_message": "API调用失败，请稍后重试",
            "success_codes": [200, 201, 202],
            "encode_json": True,
            "follow_redirects": True,
            "verify_ssl": True
        }
    ]
}

class CustomAPIManager:
    def __init__(self):
        # 将数据存储到项目根目录的data文件夹，避免被插件加载器误识别
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "custom_api")
        self.config_file = os.path.join(self.data_dir, "apis.json")
        self.system_config_file = os.path.join(self.data_dir, "system.json")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 确保配置文件夹存在
        template_dir = os.path.join(self.data_dir, "templates")
        os.makedirs(template_dir, exist_ok=True)
        
        # 先加载配置
        self.load_config()
        # 创建HTML模板
        self.create_html_template()
        
        # 启动WebUI(无论auto_open如何都启动服务器)
        self.start_webui(auto_open=self.system_config.get("auto_open_browser", False))

    def load_config(self):
        """加载配置文件"""
        try:
            # 加载系统配置
            if not os.path.exists(self.system_config_file):
                with open(self.system_config_file, "w", encoding="utf-8") as f:
                    json.dump(SYSTEM_CONFIG, f, ensure_ascii=False, indent=2)
            with open(self.system_config_file, "r", encoding="utf-8") as f:
                self.system_config = json.load(f)

            # 加载API配置
            if not os.path.exists(self.config_file):
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
                
            print("[CustomAPI]配置加载成功")
        except Exception as e:
            print(f"[CustomAPI]加载配置失败: {e}")
            self.system_config = SYSTEM_CONFIG.copy()
            self.config = DEFAULT_CONFIG.copy()

    def save_config(self):
        """保存配置到文件"""
        try:
            # 保存系统配置
            with open(self.system_config_file, "w", encoding="utf-8") as f:
                json.dump(self.system_config, f, ensure_ascii=False, indent=2)
            
            # 保存API配置
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[CustomAPI]保存配置失败: {e}")

    def start_webui(self, auto_open=True):
        """启动WebUI服务器"""
        api_manager_ref = self

        class RequestHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self2):
                if self2.path == "/" or self2.path == "/index.html":
                    self2.send_response(200)
                    self2.send_header("Content-type", "text/html; charset=utf-8")
                    self2.send_header("Access-Control-Allow-Origin", "*")
                    self2.end_headers()
                    
                    template_path = os.path.join(api_manager_ref.data_dir, "templates/index.html")
                    try:
                        with open(template_path, "r", encoding="utf-8") as f:
                            template_content = f.read()
                            self2.wfile.write(template_content.encode('utf-8'))
                    except Exception as e:
                        print(f"[CustomAPI]读取模板失败: {e}")
                        self2.wfile.write(b"Error loading template")
                        
                elif self2.path == "/config":
                    self2.send_response(200)
                    self2.send_header("Content-type", "application/json; charset=utf-8")
                    self2.send_header("Access-Control-Allow-Origin", "*")
                    self2.end_headers()
                    try:
                        # 返回完整的配置数据
                        config_data = {
                            "apis": api_manager_ref.config.get("apis", []),
                            "system": api_manager_ref.system_config
                        }
                        self2.wfile.write(json.dumps(config_data, ensure_ascii=False, indent=2).encode('utf-8'))
                    except Exception as e:
                        print(f"[CustomAPI]获取配置失败: {e}")
                        # 返回错误信息
                        self2.send_response(500)
                        self2.send_header("Content-type", "application/json")
                        self2.send_header("Access-Control-Allow-Origin", "*")
                        self2.end_headers()
                        self2.wfile.write(json.dumps({"error": str(e)}).encode())
                
            # ... 其他路由保持不变
                elif self2.path == "/bot-info":
                    self2.send_response(200)
                    self2.send_header("Content-type", "application/json")
                    self2.send_header("Access-Control-Allow-Origin", "*")
                    self2.end_headers()
                    
                    # 获取机器人信息
                    bot_info = {
                        "qq": "未定义",  # Replace with a valid value or implement a method to fetch this dynamically
                        "nickname": "机器人昵称",  # 这里需要实现获取机器人昵称的方法
                        "groupCount": 0,  # 需要实现获取群数量的方法
                        "friendCount": 0  # 需要实现获取好友数量的方法
                    }
                    self2.wfile.write(json.dumps(bot_info).encode())
                else:
                    self2.send_error(404)

            def do_POST(self2):
                if self2.path == "/save":
                    content_length = int(self2.headers['Content-Length'])
                    post_data = self2.rfile.read(content_length)
                    try:
                        new_config = json.loads(post_data.decode('utf-8'))
                        print(f"[CustomAPI]接收到配置更新: {len(new_config.get('apis', []))}个API")
                        
                        if "apis" in new_config:
                            # 更新API配置
                            api_manager_ref.config["apis"] = new_config["apis"]
                            api_manager_ref.save_config()
                            
                            self2.send_response(200)
                            self2.send_header("Content-type", "application/json; charset=utf-8")
                            self2.send_header("Access-Control-Allow-Origin", "*")
                            self2.end_headers()
                            self2.wfile.write(json.dumps({"status": "success", "message": "配置保存成功"}, ensure_ascii=False).encode('utf-8'))
                            print(f"[CustomAPI]配置保存成功")
                        else:
                            raise ValueError("Invalid config format: missing 'apis' key")
                    except json.JSONDecodeError as e:
                        print(f"[CustomAPI]JSON解析错误: {e}")
                        self2.send_response(400)
                        self2.send_header("Content-type", "application/json; charset=utf-8")
                        self2.send_header("Access-Control-Allow-Origin", "*")
                        self2.end_headers()
                        self2.wfile.write(json.dumps({"error": f"JSON格式错误: {str(e)}"}, ensure_ascii=False).encode('utf-8'))
                    except Exception as e:
                        print(f"[CustomAPI]保存配置失败: {e}")
                        self2.send_response(500)
                        self2.send_header("Content-type", "application/json; charset=utf-8")
                        self2.send_header("Access-Control-Allow-Origin", "*")
                        self2.end_headers()
                        self2.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode('utf-8'))
                else:
                    self2.send_error(404)

            def do_OPTIONS(self2):
                self2.send_response(200)
                self2.send_header("Access-Control-Allow-Origin", "*")
                self2.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self2.send_header("Access-Control-Allow-Headers", "Content-Type")
                self2.end_headers()

        # 创建HTTP服务器
        try:
            server = socketserver.TCPServer(("", self.system_config["web_port"]), RequestHandler)
        except OSError as e:
            if e.errno == 98:  # 端口已被占用
                print(f"[CustomAPI]端口 {self.system_config['web_port']} 已被占用，尝试其他端口...")
                # 尝试其他端口
                for port in range(8080, 8100):
                    try:
                        server = socketserver.TCPServer(("", port), RequestHandler)
                        self.system_config["web_port"] = port
                        self.save_config()
                        print(f"[CustomAPI]成功使用端口 {port}")
                        break
                    except OSError:
                        continue
            else:
                raise e

        def run_server():
            print(f"[CustomAPI]WebUI 服务已启动: http://localhost:{self.system_config['web_port']}")
            try:
                server.serve_forever()
            except Exception as e:
                print(f"[CustomAPI]WebUI服务出错: {e}")

        # 启动服务器线程
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # 自动打开浏览器
        if auto_open:
            webbrowser.open(f"http://localhost:{self.system_config['web_port']}")

    def create_html_template(self):
        template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>自定义API配置</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <style>
        .api-card { transition: all 0.3s ease; }
        .api-card:hover { transform: translateY(-2px); }
        .btn { transition: all 0.2s ease; }
        .btn:hover { transform: translateY(-1px); }
    </style>
</head>
<body class="bg-gray-100 p-6">
    <div class="max-w-6xl mx-auto">
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <div class="flex justify-between items-center mb-6">
                <h1 class="text-2xl font-bold">API配置管理</h1>
                <div class="space-x-4">
                    <button onclick="showHelp()" class="btn px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        使用指南
                    </button>
                    <button onclick="addApi()" class="btn px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
                        添加API
                    </button>
                    <button onclick="saveConfig()" class="btn px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600">
                        保存配置
                    </button>
                </div>
            </div>

            <!-- API列表 -->
            <div id="apiList" class="space-y-6">
                <!-- API卡片将在这里动态插入 -->
            </div>
        </div>

        # 变量说明部分 - 大幅增强的变量系统
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-bold mb-4">可用变量说明</h2>
            <div class="mb-4">
                <button onclick="toggleAllVariables()" class="btn px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
                    展开/收起所有分类
                </button>
                <button onclick="searchVariables()" class="btn px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 ml-2">
                    搜索变量
                </button>
                <input type="text" id="variableSearch" placeholder="搜索变量..." class="ml-2 p-2 border rounded">
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- 基础用户变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-blue-100 p-2 rounded" onclick="toggleCategory(this)">
                        📝 基础用户变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【用户消息】</code> - 用户发送的消息</li>
                        <li><code>【原始消息】</code> - 包含前缀的原始消息</li>
                        <li><code>【发送者QQ】</code> - 发送者QQ号</li>
                        <li><code>【发送者昵称】</code> - 发送者昵称</li>
                        <li><code>【发送人头像】</code> - 发送者QQ头像(CQ码)</li>
                        <li><code>【发送人头像链接】</code> - 发送者头像URL</li>
                        <li><code>【机器人QQ】</code> - 机器人QQ号</li>
                        <li><code>【机器人头像】</code> - 机器人头像(CQ码)</li>
                        <li><code>【机器人头像链接】</code> - 机器人头像URL</li>
                    </ul>
                </div>
                
                <!-- 群组信息变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-green-100 p-2 rounded" onclick="toggleCategory(this)">
                        👥 群组信息变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【群号】</code> - 当前群号</li>
                        <li><code>【群名称】</code> - 群组名称</li>
                        <li><code>【群人数】</code> - 当前群人数</li>
                        <li><code>【群最大人数】</code> - 群最大人数限制</li>
                    </ul>
                </div>

                <!-- 时间变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-yellow-100 p-2 rounded" onclick="toggleCategory(this)">
                        ⏰ 时间变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【当前时间】</code> - 完整日期时间</li>
                        <li><code>【年】</code> - 当前年份</li>
                        <li><code>【月】</code> - 当前月份(补零)</li>
                        <li><code>【日】</code> - 当前日期(补零)</li>
                        <li><code>【时】【分】【秒】</code> - 时分秒(补零)</li>
                        <li><code>【时分秒】</code> - HH:MM:SS格式</li>
                        <li><code>【星期】</code> - 星期几(中文)</li>
                        <li><code>【星期数字】</code> - 星期几(1-7)</li>
                        <li><code>【时间戳】</code> - Unix时间戳</li>
                        <li><code>【毫秒时间戳】</code> - 毫秒时间戳</li>
                        <li><code>【ISO时间】</code> - ISO格式时间</li>
                    </ul>
                </div>

                <!-- 系统信息变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-purple-100 p-2 rounded" onclick="toggleCategory(this)">
                        💻 系统信息变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【系统名称】</code> - 操作系统名称</li>
                        <li><code>【系统版本】</code> - 系统版本</li>
                        <li><code>【处理器】</code> - CPU信息</li>
                        <li><code>【CPU使用率】</code> - CPU使用百分比</li>
                        <li><code>【内存使用率】</code> - 内存使用百分比</li>
                        <li><code>【可用内存】</code> - 可用内存(GB)</li>
                        <li><code>【总内存】</code> - 总内存(GB)</li>
                        <li><code>【磁盘使用率】</code> - 磁盘使用百分比</li>
                        <li><code>【可用磁盘】</code> - 可用磁盘空间(GB)</li>
                        <li><code>【总磁盘】</code> - 总磁盘空间(GB)</li>
                    </ul>
                </div>

                <!-- 随机变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-red-100 p-2 rounded" onclick="toggleCategory(this)">
                        🎲 随机变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【随机数字】</code> - 1-100随机数</li>
                        <li><code>【随机数字1-10】</code> - 1-10随机数</li>
                        <li><code>【随机数字1-1000】</code> - 1-1000随机数</li>
                        <li><code>【随机UUID】</code> - UUID字符串</li>
                        <li><code>【随机字符串】</code> - 8位随机字符串</li>
                    </ul>
                </div>

                <!-- 消息处理变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-indigo-100 p-2 rounded" onclick="toggleCategory(this)">
                        ✏️ 消息处理变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【消息长度】</code> - 消息字符长度</li>
                        <li><code>【消息字数】</code> - 消息字数(不含空格)</li>
                        <li><code>【消息单词数】</code> - 英文单词数量</li>
                        <li><code>【用户消息大写】</code> - 消息转大写</li>
                        <li><code>【用户消息小写】</code> - 消息转小写</li>
                        <li><code>【用户消息首字母大写】</code> - 首字母大写</li>
                        <li><code>【用户消息反转】</code> - 消息反转</li>
                        <li><code>【跨取文本#n#m】</code> - 截取第n到m个字符</li>
                    </ul>
                </div>

                <!-- 格式化变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-teal-100 p-2 rounded" onclick="toggleCategory(this)">
                        📋 格式化变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【换行】</code> - 换行符</li>
                        <li><code>【制表符】</code> - Tab制表符</li>
                        <li><code>【空格】</code> - 单个空格</li>
                        <li><code>【at】</code> - @发送消息的用户</li>
                        <li><code>【at所有人】</code> - @全体成员</li>
                    </ul>
                </div>

                <!-- API响应变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-pink-100 p-2 rounded" onclick="toggleCategory(this)">
                        🔌 API响应变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【纯文本】</code> - API返回的文本</li>
                        <li><code>【纯图片】</code> - API返回图片显示</li>
                        <li><code>【图片链接】</code> - 原始图片URL</li>
                        <li><code>【json文本#路径】</code> - JSON中的文本值</li>
                        <li><code>【json图片#路径】</code> - JSON中的图片</li>
                    </ul>
                </div>

                <!-- 高级功能变量 -->
                <div class="variable-category">
                    <h3 class="font-semibold mb-2 cursor-pointer bg-orange-100 p-2 rounded" onclick="toggleCategory(this)">
                        ⚡ 高级功能变量 <span class="toggle-icon">▼</span>
                    </h3>
                    <ul class="variable-list list-disc pl-4 space-y-1 text-sm text-gray-600">
                        <li><code>【条件#条件表达式#真值#假值】</code> - 条件判断</li>
                        <li><code>【计算#数学表达式】</code> - 数学计算</li>
                        <li><strong>条件表达式支持:</strong> =, !=, >, <</li>
                        <li><strong>计算支持:</strong> +, -, *, /, (), 数字</li>
                    </ul>
                </div>
            </div>
            
            <!-- 变量测试区域 -->
            <div class="mt-6 bg-gray-50 p-4 rounded-lg">
                <h3 class="font-semibold mb-3">🧪 变量测试器</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block mb-2">测试模板:</label>
                        <textarea id="testTemplate" rows="4" class="w-full p-2 border rounded" 
                                  placeholder="输入包含变量的模板，如：你好【发送者昵称】，当前时间是【当前时间】"></textarea>
                    </div>
                    <div>
                        <label class="block mb-2">预览结果:</label>
                        <div id="testResult" class="w-full h-20 p-2 border rounded bg-white overflow-auto" 
                             style="min-height: 80px;">在左侧输入模板后点击测试按钮</div>
                    </div>
                </div>
                <button onclick="testVariables()" class="btn px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 mt-2">
                    🚀 测试变量
                </button>
                <button onclick="copyTestResult()" class="btn px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 mt-2 ml-2">
                    📋 复制结果
                </button>
            </div>
        </div>
    </div>

    <script>
        let config = null;

        // 加载配置
        async function loadConfig() {
            try {
                const response = await fetch('/config');
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                config = await response.json();
                console.log('配置加载成功:', config);
                await renderApis();
            } catch (error) {
                console.error('加载配置失败:', error);
                Swal.fire({
                    title: '配置加载失败',
                    text: '无法从服务器获取配置，将使用默认配置。请检查网络连接。',
                    icon: 'warning',
                    confirmButtonText: '使用默认配置'
                });
                // 使用默认配置
                config = {
                    "apis": [
                        {
                            "name": "示例API",
                            "trigger": "测试",
                            "enabled": false,
                            "use_prefix": true,
                            "read_after_command": false,
                            "url": "https://httpbin.org/post",
                            "method": "POST",
                            "headers": {
                                "Content-Type": "application/json",
                                "User-Agent": "Jianer-CustomAPI/1.0"
                            },
                            "body_template": {
                                "message": "【用户消息】",
                                "user_id": "【发送者QQ】",
                                "group_id": "【群号】",
                                "timestamp": "【时间戳】"
                            },
                            "response_template": "API返回: 【纯文本】\n发送者：【发送者昵称】\n时间：【当前时间】",
                            "cooldown": 0,
                            "timeout": 30,
                            "max_retries": 3,
                            "retry_delay": 1,
                            "error_message": "API调用失败，请稍后重试",
                            "success_codes": [200, 201, 202],
                            "encode_json": true,
                            "follow_redirects": true,
                            "verify_ssl": true
                        }
                    ]
                };
                await renderApis();
            }
        }

        // 保存配置
        async function saveConfig() {
            if (!config || !config.apis) {
                Swal.fire({
                    title: '保存失败',
                    text: '没有可保存的配置数据',
                    icon: 'error'
                });
                return;
            }

            // 显示保存中状态
            Swal.fire({
                title: '保存中...',
                text: '正在保存配置到服务器',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            try {
                const response = await fetch('/save', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(config)
                });
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
                }

                const result = await response.json();
                if (result.status === 'success') {
                    Swal.fire({
                        title: '保存成功!',
                        text: '配置已成功保存到服务器',
                        icon: 'success',
                        timer: 2000
                    });
                } else {
                    throw new Error(result.error || '保存失败');
                }
            } catch (error) {
                console.error('保存配置失败:', error);
                Swal.fire({
                    title: '保存失败!',
                    text: error.message || '网络连接异常，请检查服务器状态',
                    icon: 'error',
                    confirmButtonText: '确定'
                });
            }
        }

        // 渲染API列表
        function renderApis() {
            const apiList = document.getElementById('apiList');
            if (!apiList) {
                console.error('apiList 元素不存在');
                return;
            }

            if (!config || !config.apis) {
                console.warn('配置数据不存在或格式错误');
                config = { apis: [] };
            }
            
            if (config.apis.length === 0) {
                apiList.innerHTML = `
                    <div class="text-center py-12">
                        <p class="text-gray-500 text-lg mb-4">暂无API配置</p>
                        <button onclick="addApi()" class="btn px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600">
                            添加第一个API
                        </button>
                    </div>
                `;
                return;
            }
            
            apiList.innerHTML = config.apis.map((api, index) => {
                // 确保所有必要属性都存在
                const safeApi = {
                    name: api.name || '未命名API',
                    trigger: api.trigger || 'test',
                    enabled: api.enabled || false,
                    use_prefix: api.use_prefix !== false,
                    read_after_command: api.read_after_command || false,
                    url: api.url || 'https://example.com/api',
                    method: api.method || 'GET',
                    cooldown: api.cooldown || 0,
                    timeout: api.timeout || 30,
                    max_retries: api.max_retries || 3,
                    retry_delay: api.retry_delay || 1,
                    encode_json: api.encode_json !== false,
                    follow_redirects: api.follow_redirects !== false,
                    verify_ssl: api.verify_ssl !== false,
                    response_template: api.response_template || 'API返回: 【纯文本】',
                    error_message: api.error_message || 'API调用失败，请稍后重试',
                    headers: api.headers || { 'Content-Type': 'application/json' },
                    body_template: api.body_template || {}
                };

                return `
                <div class="api-card bg-gray-50 rounded-lg p-4 border">
                    <div class="flex justify-between mb-4">
                        <input type="text" value="${safeApi.name}" 
                               onchange="updateApi(${index}, 'name', this.value)"
                               class="text-xl font-bold bg-transparent border-b border-gray-300 focus:outline-none focus:border-blue-500">
                        <label class="flex items-center">
                            <input type="checkbox" ${safeApi.enabled ? 'checked' : ''} 
                                   onchange="updateApi(${index}, 'enabled', this.checked)"
                                   class="mr-2">
                            启用
                        </label>
                    </div>

                    <div class="grid grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block mb-1">触发指令</label>
                            <input type="text" value="${safeApi.trigger}" 
                                   onchange="updateApi(${index}, 'trigger', this.value)"
                                   class="w-full p-2 border rounded">
                        </div>
                        <div class="flex items-center">
                            <label class="flex items-center">
                                <input type="checkbox" ${safeApi.use_prefix ? 'checked' : ''} 
                                       onchange="updateApi(${index}, 'use_prefix', this.checked)"
                                       class="mr-2">
                                使用指令前缀
                            </label>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <label class="block mb-1">API URL</label>
                            <input type="text" value="${safeApi.url}" 
                                   onchange="updateApi(${index}, 'url', this.value)"
                                   class="w-full p-2 border rounded">
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block mb-1">请求方法</label>
                                <select onchange="updateApi(${index}, 'method', this.value)"
                                        class="w-full p-2 border rounded">
                                    <option value="GET" ${safeApi.method === 'GET' ? 'selected' : ''}>GET</option>
                                    <option value="POST" ${safeApi.method === 'POST' ? 'selected' : ''}>POST</option>
                                    <option value="PUT" ${safeApi.method === 'PUT' ? 'selected' : ''}>PUT</option>
                                    <option value="DELETE" ${safeApi.method === 'DELETE' ? 'selected' : ''}>DELETE</option>
                                    <option value="PATCH" ${safeApi.method === 'PATCH' ? 'selected' : ''}>PATCH</option>
                                    <option value="HEAD" ${safeApi.method === 'HEAD' ? 'selected' : ''}>HEAD</option>
                                </select>
                            </div>
                            <div>
                                <label class="block mb-1">冷却时间(秒)</label>
                                <input type="number" value="${safeApi.cooldown}" min="0"
                                       onchange="updateApi(${index}, 'cooldown', parseInt(this.value))"
                                       class="w-full p-2 border rounded">
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block mb-1">超时时间(秒)</label>
                                <input type="number" value="${safeApi.timeout}" min="1" max="300"
                                       onchange="updateApi(${index}, 'timeout', parseInt(this.value))"
                                       class="w-full p-2 border rounded">
                            </div>
                            <div>
                                <label class="block mb-1">最大重试次数</label>
                                <input type="number" value="${safeApi.max_retries}" min="0" max="10"
                                       onchange="updateApi(${index}, 'max_retries', parseInt(this.value))"
                                       class="w-full p-2 border rounded">
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-4">
                            <div class="flex items-center">
                                <label class="flex items-center">
                                    <input type="checkbox" ${safeApi.encode_json ? 'checked' : ''} 
                                           onchange="updateApi(${index}, 'encode_json', this.checked)"
                                           class="mr-2">
                                    JSON编码
                                </label>
                            </div>
                            <div class="flex items-center">
                                <label class="flex items-center">
                                    <input type="checkbox" ${safeApi.follow_redirects ? 'checked' : ''} 
                                           onchange="updateApi(${index}, 'follow_redirects', this.checked)"
                                           class="mr-2">
                                    跟随重定向
                                </label>
                            </div>
                            <div class="flex items-center">
                                <label class="flex items-center">
                                    <input type="checkbox" ${safeApi.verify_ssl ? 'checked' : ''} 
                                           onchange="updateApi(${index}, 'verify_ssl', this.checked)"
                                           class="mr-2">
                                    SSL验证
                                </label>
                            </div>
                        </div>

                        <div>
                            <label class="block mb-1">响应模板</label>
                            <textarea onchange="updateApi(${index}, 'response_template', this.value)"
                                      class="w-full p-2 border rounded h-20">${safeApi.response_template}</textarea>
                        </div>

                        <div>
                            <label class="block mb-1">错误消息模板</label>
                            <textarea onchange="updateApi(${index}, 'error_message', this.value)"
                                      class="w-full p-2 border rounded h-16" 
                                      placeholder="API调用失败时显示的错误消息">${safeApi.error_message}</textarea>
                        </div>

                        <div class="flex items-center mb-4">
                            <label class="flex items-center">
                                <input type="checkbox" ${safeApi.read_after_command ? 'checked' : ''} 
                                       onchange="updateApi(${index}, 'read_after_command', this.checked)"
                                       class="mr-2">
                                读取指令后消息
                            </label>
                        </div>

                        <div>
                            <label class="block mb-1">请求头(Headers)</label>
                            <textarea onchange="updateApiHeaders(${index}, this.value)"
                                      class="w-full p-2 border rounded h-20">${JSON.stringify(safeApi.headers, null, 2)}</textarea>
                            <p class="text-sm text-gray-500 mt-1">JSON格式,例如: {"Content-Type": "application/json"}</p>
                        </div>

                        <div>
                            <label class="block mb-1">请求体模板(Body)</label>
                            <textarea onchange="updateApiBody(${index}, this.value)"
                                      class="w-full p-2 border rounded h-20">${JSON.stringify(safeApi.body_template, null, 2)}</textarea>
                            <p class="text-sm text-gray-500 mt-1">JSON格式,支持使用变量</p>
                        </div>

                    </div>

                    <div class="flex justify-end space-x-2 mt-4">
                        <button onclick="testApi(${index})"
                                class="btn px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                            测试API
                        </button>
                        <button onclick="duplicateApi(${index})"
                                class="btn px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600">
                            复制
                        </button>
                        <button onclick="deleteApi(${index})"
                                class="btn px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
                            删除
                        </button>
                    </div>
                </div>
            `}).join('');
        }

        // 更新API
        function updateApi(index, key, value) {
            if (!config || !config.apis || !config.apis[index]) {
                console.error('API不存在:', index);
                return;
            }
            config.apis[index][key] = value;
            console.log(`更新API ${index}.${key} = ${value}`);
        }

        // 更新Headers(安全JSON解析)
        function updateApiHeaders(index, value) {
            try {
                const headers = JSON.parse(value);
                updateApi(index, 'headers', headers);
            } catch (error) {
                console.error('请求头JSON格式错误:', error);
                Swal.fire({
                    title: 'JSON格式错误',
                    text: '请检查请求头的JSON格式是否正确',
                    icon: 'error',
                    timer: 3000
                });
            }
        }

        // 更新Body(安全JSON解析)
        function updateApiBody(index, value) {
            try {
                const body = JSON.parse(value);
                updateApi(index, 'body_template', body);
            } catch (error) {
                console.error('请求体JSON格式错误:', error);
                Swal.fire({
                    title: 'JSON格式错误',
                    text: '请检查请求体的JSON格式是否正确',
                    icon: 'error',
                    timer: 3000
                });
            }
        }

        // 测试API功能
        function testApi(index) {
            if (!config || !config.apis || !config.apis[index]) {
                Swal.fire({
                    title: 'API不存在',
                    text: '无法找到指定的API配置',
                    icon: 'error'
                });
                return;
            }

            const api = config.apis[index];
            Swal.fire({
                title: 'API测试',
                html: `
                    <div class="text-left space-y-2">
                        <p><strong>API名称:</strong> ${api.name}</p>
                        <p><strong>触发指令:</strong> ${api.trigger}</p>
                        <p><strong>请求方法:</strong> ${api.method}</p>
                        <p><strong>URL:</strong> ${api.url}</p>
                        <p><strong>启用状态:</strong> ${api.enabled ? '已启用' : '未启用'}</p>
                        <hr>
                        <p class="text-sm text-gray-600">注意：这只是配置预览，实际测试需要在QQ群中发送指令</p>
                    </div>
                `,
                confirmButtonText: '知道了'
            });
        }

        // 复制API
        function duplicateApi(index) {
            if (!config || !config.apis || !config.apis[index]) {
                Swal.fire({
                    title: 'API不存在',
                    text: '无法找到指定的API配置',
                    icon: 'error'
                });
                return;
            }

            const originalApi = config.apis[index];
            const duplicatedApi = JSON.parse(JSON.stringify(originalApi)); // 深拷贝
            duplicatedApi.name = originalApi.name + ' (副本)';
            duplicatedApi.trigger = originalApi.trigger + '_copy';
            duplicatedApi.enabled = false; // 副本默认禁用

            config.apis.push(duplicatedApi);
            renderApis();
            
            // 滚动到新添加的API
            setTimeout(() => {
                window.scrollTo(0, document.body.scrollHeight);
            }, 100);

            Swal.fire({
                title: 'API已复制',
                text: '请修改副本的名称和触发指令',
                icon: 'success',
                timer: 2000
            });
        }

        // 添加新API
        async function addApi() {
            const result = await Swal.fire({
                title: '添加新API',
                html: `
                    <div class="space-y-4">
                        <input id="apiName" class="w-full p-2 border rounded" 
                            placeholder="API名称">
                        <input id="apiTrigger" class="w-full p-2 border rounded" 
                            placeholder="触发指令">
                    </div>
                `,
                showCancelButton: true,
                confirmButtonText: '添加',
                cancelButtonText: '取消'
            });

            if (result.isConfirmed) {
                const name = document.getElementById('apiName').value || "新API";
                const trigger = document.getElementById('apiTrigger').value || "测试";
                
                config.apis.push({
                    name: name,
                    trigger: trigger,
                    enabled: false,
                    use_prefix: true,
                    read_after_command: false,
                    url: "https://example.com/api",
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "User-Agent": "Jianer-CustomAPI/1.0"
                    },
                    body_template: {
                        "message": "【用户消息】",
                        "user_id": "【发送者QQ】",
                        "group_id": "【群号】",
                        "timestamp": "【时间戳】"
                    },
                    response_template: "API返回: 【纯文本】\n发送者：【发送者昵称】\n时间：【当前时间】",
                    cooldown: 0,
                    timeout: 30,
                    max_retries: 3,
                    retry_delay: 1,
                    error_message: "API调用失败，请稍后重试",
                    success_codes: [200, 201, 202],
                    encode_json: true,
                    follow_redirects: true,
                    verify_ssl: true
                });
                
                renderApis();
                // 滚动到新添加的API
                window.scrollTo(0, document.body.scrollHeight);
                
                Swal.fire({
                    title: 'API已添加',
                    text: '请完善API配置并保存',
                    icon: 'success',
                    timer: 2000
                });
            }
        }

        // 删除API
        function deleteApi(index) {
            Swal.fire({
                title: '确认删除?',
                text: `确定要删除 "${config.apis[index].name}" 吗？`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: '删除',
                cancelButtonText: '取消'
            }).then((result) => {
                if (result.isConfirmed) {
                    config.apis.splice(index, 1);
                    renderApis();
                }
            });
        }

        // 显示帮助
        function showHelp() {
            Swal.fire({
                title: '使用指南',
                html: `
                    <div class="text-left space-y-4">
                        <p>1. 点击"添加API"创建新的API配置</p>
                        <p>2. 填写API基本信息(名称、触发指令)</p>
                        <p>3. 设置API请求参数(URL、方法等)</p>
                        <p>4. 使用响应模板定制返回内容</p>
                        <p>5. 点击"保存配置"保存更改</p>
                        <p><strong>新功能:</strong> 使用变量测试器测试变量效果！</p>
                    </div>
                `,
                confirmButtonText: '知道了'
            });
        }

        // 变量分类展开/收起功能
        function toggleCategory(element) {
            const list = element.nextElementSibling;
            const icon = element.querySelector('.toggle-icon');
            if (list.style.display === 'none') {
                list.style.display = 'block';
                icon.textContent = '▼';
            } else {
                list.style.display = 'none';
                icon.textContent = '▶';
            }
        }

        function toggleAllVariables() {
            const categories = document.querySelectorAll('.variable-category');
            const firstList = categories[0].querySelector('.variable-list');
            const shouldShow = firstList.style.display === 'none';
            
            categories.forEach(category => {
                const list = category.querySelector('.variable-list');
                const icon = category.querySelector('.toggle-icon');
                list.style.display = shouldShow ? 'block' : 'none';
                icon.textContent = shouldShow ? '▼' : '▶';
            });
        }

        function searchVariables() {
            const searchTerm = document.getElementById('variableSearch').value.toLowerCase();
            const categories = document.querySelectorAll('.variable-category');
            
            categories.forEach(category => {
                const items = category.querySelectorAll('li');
                let hasVisibleItems = false;
                
                items.forEach(item => {
                    if (searchTerm === '' || item.textContent.toLowerCase().includes(searchTerm)) {
                        item.style.display = 'list-item';
                        hasVisibleItems = true;
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                // 显示/隐藏分类
                category.style.display = hasVisibleItems || searchTerm === '' ? 'block' : 'none';
                
                // 如果有搜索结果，展开分类
                if (hasVisibleItems && searchTerm !== '') {
                    const list = category.querySelector('.variable-list');
                    const icon = category.querySelector('.toggle-icon');
                    list.style.display = 'block';
                    icon.textContent = '▼';
                }
            });
        }

        function testVariables() {
            const template = document.getElementById('testTemplate').value;
            if (!template.trim()) {
                document.getElementById('testResult').innerHTML = '请输入模板内容';
                return;
            }
            
            // 模拟变量替换（用于测试显示）
            let result = template;
            const mockData = {
                '【用户消息】': '测试消息内容',
                '【原始消息】': '-测试消息内容',
                '【发送者QQ】': '123456789',
                '【发送者昵称】': '测试用户',
                '【群号】': '987654321',
                '【群名称】': '测试群组',
                '【群人数】': '50',
                '【机器人QQ】': '3456789012',
                '【当前时间】': new Date().toLocaleString('zh-CN'),
                '【年】': new Date().getFullYear().toString(),
                '【月】': (new Date().getMonth() + 1).toString().padStart(2, '0'),
                '【日】': new Date().getDate().toString().padStart(2, '0'),
                '【时】': new Date().getHours().toString().padStart(2, '0'),
                '【分】': new Date().getMinutes().toString().padStart(2, '0'),
                '【秒】': new Date().getSeconds().toString().padStart(2, '0'),
                '【时分秒】': new Date().toTimeString().substring(0, 8),
                '【星期】': ['日', '一', '二', '三', '四', '五', '六'][new Date().getDay()],
                '【系统名称】': 'Windows',
                '【CPU使用率】': '15.6%',
                '【内存使用率】': '68.2%',
                '【随机数字】': Math.floor(Math.random() * 100 + 1).toString(),
                '【随机数字1-10】': Math.floor(Math.random() * 10 + 1).toString(),
                '【消息长度】': '测试消息内容'.length.toString(),
                '【消息字数】': '测试消息内容'.replace(/\s/g, '').length.toString(),
                '【用户消息大写】': '测试消息内容'.toUpperCase(),
                '【用户消息小写】': '测试消息内容'.toLowerCase(),
                '【机器人名称】': '简儿',
                '【触发前缀】': '-',
                '【换行】': '\n',
                '【空格】': ' ',
                '【at】': '@测试用户',
                '【纯文本】': 'API返回的文本内容',
                '【json文本#data.message】': 'JSON中的文本内容'
            };
            
            // 处理跨取文本
            const crossMatches = result.match(/【跨取文本#(\d+)#(\d+)】/g);
            if (crossMatches) {
                crossMatches.forEach(match => {
                    const nums = match.match(/\d+/g);
                    if (nums && nums.length >= 2) {
                        const start = parseInt(nums[0]);
                        const end = parseInt(nums[1]);
                        const text = '测试消息内容';
                        const extracted = text.substring(start - 1, end);
                        result = result.replace(match, extracted);
                    }
                });
            }
            
            // 处理条件变量
            const conditionMatches = result.match(/【条件#([^#]+)#([^#]*)#([^】]*)】/g);
            if (conditionMatches) {
                conditionMatches.forEach(match => {
                    const parts = match.match(/【条件#([^#]+)#([^#]*)#([^】]*)】/);
                    if (parts) {
                        const condition = parts[1];
                        const trueVal = parts[2];
                        const falseVal = parts[3];
                        // 简单模拟条件判断
                        let conditionResult = false;
                        if (condition.includes('=')) {
                            conditionResult = Math.random() > 0.5; // 随机结果用于演示
                        }
                        result = result.replace(match, conditionResult ? trueVal : falseVal);
                    }
                });
            }
            
            // 处理计算变量
            const calcMatches = result.match(/【计算#([^】]+)】/g);
            if (calcMatches) {
                calcMatches.forEach(match => {
                    const expr = match.match(/【计算#([^】]+)】/)[1];
                    try {
                        // 安全计算（仅用于演示）
                        if (/^[0-9+\\-*/.() ]+$/.test(expr)) {
                            const calcResult = eval(expr);
                            result = result.replace(match, calcResult.toString());
                        } else {
                            result = result.replace(match, '表达式错误');
                        }
                    } catch (e) {
                        result = result.replace(match, '计算失败');
                    }
                });
            }
            
            // 替换所有模拟数据
            for (const [key, value] of Object.entries(mockData)) {
                result = result.replace(new RegExp(key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), value);
            }
            
            document.getElementById('testResult').innerHTML = result.replace(/\n/g, '<br>');
        }

        function copyTestResult() {
            const result = document.getElementById('testResult').innerText;
            navigator.clipboard.writeText(result).then(() => {
                Swal.fire({
                    title: '复制成功',
                    icon: 'success',
                    timer: 1000
                });
            }).catch(() => {
                Swal.fire({
                    title: '复制失败',
                    text: '请手动复制结果',
                    icon: 'error'
                });
            });
        }

        // 初始化
        window.addEventListener('load', function() {
            loadConfig();
            
            // 搜索框实时搜索
            const searchInput = document.getElementById('variableSearch');
            if (searchInput) {
                searchInput.addEventListener('input', searchVariables);
            }
        });
    </script>
</body>
</html>
"""
        template_path = os.path.join(self.data_dir, "templates/index.html")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template)

api_manager = CustomAPIManager()

async def process_template(template, data, event, actions, api=None):
    """处理模板变量 - 增强版支持大量变量类型"""
    try:
        result = template
        message = str(event.message)
        reminder = Configurator.cm.get_cfg().others['reminder']
        
        # 获取用户消息
        if api and api.get("read_after_command", False):
            # 如果开启了"读取指令后消息"选项
            trigger = f"{reminder}{api['trigger']}" if api.get("use_prefix", True) else api['trigger']
            user_message = message[len(trigger):].strip() if message.startswith(trigger) else message
        else:
            # 否则获取完整消息
            user_message = message

        # 获取当前时间
        now = datetime.now()

        # 处理跨取文本
        cross_matches = re.findall(r'【跨取文本#(\d+)#(\d+)】', result)
        for start, end in cross_matches:
            try:
                start_idx = int(start) - 1
                end_idx = int(end)
                if start_idx >= 0 and end_idx <= len(user_message):
                    cross_text = user_message[start_idx:end_idx]
                    result = result.replace(f"【跨取文本#{start}#{end}】", cross_text)
            except Exception as e:
                print(f"[CustomAPI]处理跨取文本失败 {start}-{end}: {e}")
                result = result.replace(f"【跨取文本#{start}#{end}】", "获取失败")

        # 获取用户信息
        try:
            user_info = await actions.get_stranger_info(event.user_id)
            user_nickname = user_info.data.raw.get("nickname", "未知用户")
        except:
            user_nickname = "未知用户"
        
        # 获取群信息
        group_name = ""
        group_member_count = 0
        group_max_member_count = 0
        if hasattr(event, 'group_id') and event.group_id:
            try:
                group_info = await actions.get_group_info(event.group_id)
                group_name = group_info.data.raw.get("group_name", "")
                group_member_count = group_info.data.raw.get("member_count", 0)
                group_max_member_count = group_info.data.raw.get("max_member_count", 0)
            except:
                pass

        # 获取系统信息
        import psutil
        import platform
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 处理变量替换 - 大幅增强的变量系统
        replacements = {
            # === 基础用户变量 ===
            "【用户消息】": user_message,
            "【原始消息】": message,
            "【发送者QQ】": str(event.user_id),
            "【发送者昵称】": user_nickname,
            "【发送人头像】": f"[CQ:image,file=http://q1.qlogo.cn/g?b=qq&nk={event.user_id}&s=640]",
            "【发送人头像链接】": f"http://q1.qlogo.cn/g?b=qq&nk={event.user_id}&s=640",
            "【机器人QQ】": str(event.self_id),
            "【机器人头像】": f"[CQ:image,file=http://q1.qlogo.cn/g?b=qq&nk={event.self_id}&s=640]",
            "【机器人头像链接】": f"http://q1.qlogo.cn/g?b=qq&nk={event.self_id}&s=640",
            
            # === 群组信息变量 ===
            "【群号】": str(getattr(event, 'group_id', '')),
            "【群名称】": group_name,
            "【群人数】": str(group_member_count),
            "【群最大人数】": str(group_max_member_count),
            
            # === 时间变量 ===
            "【当前时间】": now.strftime("%Y-%m-%d %H:%M:%S"),
            "【年】": str(now.year),
            "【月】": str(now.month).zfill(2),
            "【日】": str(now.day).zfill(2),
            "【时】": str(now.hour).zfill(2),
            "【分】": str(now.minute).zfill(2),
            "【秒】": str(now.second).zfill(2),
            "【时分秒】": now.strftime("%H:%M:%S"),
            "【星期】": ["一", "二", "三", "四", "五", "六", "日"][now.weekday()],
            "【星期数字】": str(now.weekday() + 1),
            "【时间戳】": str(int(now.timestamp())),
            "【毫秒时间戳】": str(int(now.timestamp() * 1000)),
            "【ISO时间】": now.isoformat(),
            "【UTC时间】": now.utctimetuple(),
            
            # === 系统信息变量 ===
            "【系统名称】": platform.system(),
            "【系统版本】": platform.release(),
            "【处理器】": platform.processor(),
            "【CPU使用率】": f"{cpu_percent:.1f}%",
            "【内存使用率】": f"{memory.percent:.1f}%",
            "【可用内存】": f"{memory.available // (1024**3):.1f}GB",
            "【总内存】": f"{memory.total // (1024**3):.1f}GB",
            "【磁盘使用率】": f"{disk.percent:.1f}%",
            "【可用磁盘】": f"{disk.free // (1024**3):.1f}GB",
            "【总磁盘】": f"{disk.total // (1024**3):.1f}GB",
            
            # === 消息格式变量 ===
            "【换行】": "\n",
            "【制表符】": "\t",
            "【空格】": " ",
            "【at】": f"[CQ:at,qq={event.user_id}]",
            "【at所有人】": "[CQ:at,qq=all]",
            
            # === 随机变量 ===
            "【随机数字】": str(random.randint(1, 100)),
            "【随机数字1-10】": str(random.randint(1, 10)),
            "【随机数字1-1000】": str(random.randint(1, 1000)),
            "【随机UUID】": str(uuid.uuid4()),
            "【随机字符串】": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8)),
            
            # === 特殊功能变量 ===
            "【消息长度】": str(len(user_message)),
            "【消息字数】": str(len(user_message.replace(' ', ''))),
            "【消息单词数】": str(len(user_message.split())),
            "【用户消息大写】": user_message.upper(),
            "【用户消息小写】": user_message.lower(),
            "【用户消息首字母大写】": user_message.capitalize(),
            "【用户消息反转】": user_message[::-1],
            
            # === 配置信息变量 ===
            "【机器人名称】": Configurator.cm.get_cfg().basic.get('bot_name', '简儿'),
            "【触发前缀】": reminder,
            "【API名称】": api.get('name', '未知API') if api else '未知API',
            "【API触发词】": api.get('trigger', '') if api else '',
        }
        
        # 处理纯文本和纯图片响应
        if isinstance(data, str):
            # 检查响应是否是图片URL
            image_url = None
            if data.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                image_url = data
            elif data.startswith('http') and await is_image_url(data):
                # 如果是重定向链接,获取真实图片URL
                image_url = await get_real_image_url(data)
            
            if image_url:
                if "【纯图片】" in result:
                    result = result.replace("【纯图片】", f"[CQ:image,file={image_url}]")
                if "【图片链接】" in result:
                    result = result.replace("【图片链接】", image_url)
            else:
                # 非图片URL则作为纯文本处理
                result = result.replace("【纯文本】", data)
                if "【纯图片】" in result:
                    result = result.replace("【纯图片】", "[CQ:image,file=" + data + "]" if data.startswith('http') else data)
                if "【图片链接】" in result:
                    result = result.replace("【图片链接】", data if data.startswith('http') else "")

        # 处理 JSON 路径变量
        if isinstance(data, dict):
            # 处理JSON中的图片和文本
            json_matches = re.findall(r'【json(图片|文本)#([^】]+)】', result)
            for match_type, json_path in json_matches:
                try:
                    value = data
                    for key in json_path.split('.'):
                        if key.isdigit():  # 处理数组索引
                            value = value[int(key)]
                        else:
                            value = value[key]
                    
                    if match_type == "图片" and isinstance(value, str):
                        image_url = None
                        if value.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                            image_url = value  
                        elif value.startswith('http') and await is_image_url(value):
                            image_url = await get_real_image_url(value)

                        if image_url:
                            result = result.replace(f"【json图片#{json_path}】", 
                                f"[CQ:image,file={image_url}]")
                        else:
                            print(f"[CustomAPI]警告: JSON路径 {json_path} 的值不是有效的图片URL")
                            result = result.replace(f"【json图片#{json_path}】", "非图片URL")
                    else:
                        result = result.replace(f"【json文本#{json_path}】", str(value))
                except Exception as e:
                    print(f"[CustomAPI]处理JSON路径失败 {json_path}: {e}")
                    result = result.replace(f"【json{match_type}#{json_path}】", "获取失败")

        # 处理条件变量 【条件#条件表达式#真值#假值】
        condition_matches = re.findall(r'【条件#([^#]+)#([^#]*)#([^】]*)】', result)
        for condition, true_val, false_val in condition_matches:
            try:
                # 简单的条件判断支持
                condition_result = False
                if "=" in condition:
                    left, right = condition.split("=", 1)
                    left = left.strip()
                    right = right.strip()
                    # 替换左侧变量
                    for key, value in replacements.items():
                        left = left.replace(key, str(value))
                    condition_result = (left == right)
                elif "!=" in condition:
                    left, right = condition.split("!=", 1)
                    left = left.strip()
                    right = right.strip()
                    for key, value in replacements.items():
                        left = left.replace(key, str(value))
                    condition_result = (left != right)
                elif ">" in condition:
                    left, right = condition.split(">", 1)
                    left = left.strip()
                    right = right.strip()
                    for key, value in replacements.items():
                        left = left.replace(key, str(value))
                    try:
                        condition_result = (float(left) > float(right))
                    except:
                        condition_result = False
                elif "<" in condition:
                    left, right = condition.split("<", 1)
                    left = left.strip()
                    right = right.strip()
                    for key, value in replacements.items():
                        left = left.replace(key, str(value))
                    try:
                        condition_result = (float(left) < float(right))
                    except:
                        condition_result = False
                
                final_val = true_val if condition_result else false_val
                result = result.replace(f"【条件#{condition}#{true_val}#{false_val}】", final_val)
            except Exception as e:
                print(f"[CustomAPI]处理条件变量失败 {condition}: {e}")
                result = result.replace(f"【条件#{condition}#{true_val}#{false_val}】", "条件处理失败")

        # 处理计算变量 【计算#表达式】
        calc_matches = re.findall(r'【计算#([^】]+)】', result)
        for calc_expr in calc_matches:
            try:
                # 替换表达式中的变量
                expr = calc_expr
                for key, value in replacements.items():
                    if key in expr:
                        try:
                            # 尝试转换为数字
                            num_val = float(str(value).replace('%', '').replace('GB', ''))
                            expr = expr.replace(key, str(num_val))
                        except:
                            expr = expr.replace(key, str(value))
                
                # 安全计算（只允许基本数学运算）
                allowed_chars = set('0123456789+-*/.() ')
                if all(c in allowed_chars for c in expr):
                    calc_result = eval(expr)
                    result = result.replace(f"【计算#{calc_expr}】", str(calc_result))
                else:
                    result = result.replace(f"【计算#{calc_expr}】", "表达式包含非法字符")
            except Exception as e:
                print(f"[CustomAPI]处理计算变量失败 {calc_expr}: {e}")
                result = result.replace(f"【计算#{calc_expr}】", "计算失败")

        # 替换所有基础变量
        for key, value in replacements.items():
            result = result.replace(key, str(value))

        return result

    except Exception as e:
        print(f"[CustomAPI]处理模板失败: {e}")
        return f"模板处理失败：{str(e)}"

# 辅助函数:处理HTTP响应
async def handle_response(response, success_codes, head_request=False):
    """
    处理HTTP响应，支持多种内容类型和状态码检查
    """
    # 检查状态码
    if response.status not in success_codes:
        raise aiohttp.ClientResponseError(
            request_info=response.request_info,
            history=response.history,
            status=response.status,
            message=f"HTTP {response.status}: {response.reason}",
            headers=response.headers
        )
    
    # HEAD请求只返回响应头信息
    if head_request:
        return {
            "status": response.status,
            "headers": dict(response.headers),
            "content_type": response.headers.get("Content-Type", "")
        }, response.headers.get("Content-Type", "")
    
    content_type = response.headers.get("Content-Type", "").lower()
    
    try:
        if "application/json" in content_type:
            data = await response.json()
        elif "text/" in content_type or "application/xml" in content_type:
            data = await response.text()
        elif content_type.startswith("image/"):
            # 对于图片类型，返回URL
            data = str(response.url)
        else:
            # 其他类型尝试作为文本处理
            try:
                data = await response.text()
            except UnicodeDecodeError:
                # 如果无法解码为文本，返回字节数据的十六进制表示
                data = (await response.read()).hex()
                
        return data, content_type
        
    except Exception as e:
        print(f"[CustomAPI]解析响应失败: {e}")
        # 作为文本返回原始内容
        try:
            data = await response.text()
        except:
            data = f"响应解析失败: {str(e)}"
        return data, content_type

# 辅助函数:检查URL是否为图片
async def is_image_url(url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, allow_redirects=True) as response:
                content_type = response.headers.get('content-type', '')
                return content_type.startswith('image/')
    except:
        return False

# 辅助函数:获取重定向后的真实图片URL
async def get_real_image_url(url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=True) as response:
                return str(response.url)
    except:
        return url

async def check_permission(event):
    """检查用户权限"""
    try:
        user_id = str(event.user_id)
        cfg = Configurator.cm.get_cfg()
        
        # 1. 检查 owner
        if user_id in [str(x) for x in cfg.owner]:
            print(f"[CustomAPI]用户{user_id}在owner列表中")
            return True
            
        # 2. 检查 ROOT_User
        if user_id in [str(x) for x in cfg.others['ROOT_User']]:
            print(f"[CustomAPI]用户{user_id}在ROOT_User列表中")
            return True
        
        # 3. 检查 Super_User.ini
        try:
            with open("Super_User.ini", "r", encoding='utf-8') as f:
                super_users = [str(x.strip()) for x in f.read().splitlines() if x.strip()]
                if user_id in super_users:
                    print(f"[CustomAPI]用户{user_id}在Super_User.ini中")
                    return True
        except Exception as e:
            print(f"[CustomAPI]读取Super_User.ini失败: {e}")
            
        # 4. 检查 Manage_User.ini
        try:
            with open("Manage_User.ini", "r", encoding='utf-8') as f:
                manage_users = [str(x.strip()) for x in f.read().splitlines() if x.strip()]
                if user_id in manage_users:
                    print(f"[CustomAPI]用户{user_id}在Manage_User.ini中")
                    return True
        except Exception as e:
            print(f"[CustomAPI]读取Manage_User.ini失败: {e}")
        
        print(f"[CustomAPI]用户{user_id}权限检查未通过")
        return False
        
    except Exception as e:
        print(f"[CustomAPI]权限检查出错: {e}")
        return False

async def on_message(event, actions, Manager, Segments):
    if not hasattr(event, 'message'):
        return False
        
    message = str(event.message)
    reminder = Configurator.cm.get_cfg().others['reminder']
    
    # WebUI控制指令
    if message == f"{reminder}打开自定义API配置":
        if not await check_permission(event):
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("你没有权限执行此操作"))
            )
            return True
        webbrowser.open(f"http://localhost:{api_manager.system_config['web_port']}")
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(f"WebUI已打开: http://localhost:{api_manager.system_config['web_port']}"))
        )
        return True
    
    # 设置自动打开
    elif message == f"{reminder}设置自动打开API配置":
        if not await check_permission(event):
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text("你没有权限执行此操作"))
            )
            return True
        api_manager.system_config["auto_open_browser"] = not api_manager.system_config["auto_open_browser"]
        api_manager.save_config()
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(f"自动打开WebUI已{'开启' if api_manager.system_config["auto_open_browser"] else '关闭'}"))
        )
        return True
    
    message = str(event.message)
    reminder = Configurator.cm.get_cfg().others['reminder']
    
    for api in api_manager.config["apis"]:
        if not api["enabled"]:
            continue
            
        trigger = f"{reminder}{api['trigger']}" if api["use_prefix"] else api["trigger"]
        
        if not message.startswith(trigger):
            continue
            
        try:
            # 处理 URL 模板变量
            url = await process_template(api["url"], None, event, actions, api)
            
            # 处理请求体模板
            body = {}
            if isinstance(api["body_template"], dict):
                body = api["body_template"].copy()
                for key, value in body.items():
                    body[key] = await process_template(value, None, event, actions, api)
            
            # 获取API配置参数
            method = api.get("method", "GET").upper()
            timeout = api.get("timeout", 30)
            max_retries = api.get("max_retries", 3)
            retry_delay = api.get("retry_delay", 1)
            success_codes = api.get("success_codes", [200, 201, 202])
            follow_redirects = api.get("follow_redirects", True)
            verify_ssl = api.get("verify_ssl", True)
            encode_json = api.get("encode_json", True)
            
            # 重试机制
            last_error = None
            for attempt in range(max_retries + 1):
                try:
                    # 创建 HTTP 客户端
                    connector = aiohttp.TCPConnector(
                        ssl=verify_ssl,
                        limit=100,
                        limit_per_host=10
                    )
                    
                    timeout_config = aiohttp.ClientTimeout(total=timeout)
                    
                    async with aiohttp.ClientSession(
                        connector=connector,
                        timeout=timeout_config
                    ) as session:
                        headers = api["headers"].copy()
                        
                        # 根据方法发送请求
                        if method == "GET":
                            async with session.get(
                                url, 
                                params=body, 
                                headers=headers,
                                allow_redirects=follow_redirects
                            ) as response:
                                data, content_type = await handle_response(response, success_codes)
                                
                        elif method == "POST":
                            if encode_json:
                                async with session.post(
                                    url, 
                                    json=body, 
                                    headers=headers,
                                    allow_redirects=follow_redirects
                                ) as response:
                                    data, content_type = await handle_response(response, success_codes)
                            else:
                                async with session.post(
                                    url, 
                                    data=body, 
                                    headers=headers,
                                    allow_redirects=follow_redirects
                                ) as response:
                                    data, content_type = await handle_response(response, success_codes)
                                    
                        elif method == "PUT":
                            if encode_json:
                                async with session.put(
                                    url, 
                                    json=body, 
                                    headers=headers,
                                    allow_redirects=follow_redirects
                                ) as response:
                                    data, content_type = await handle_response(response, success_codes)
                            else:
                                async with session.put(
                                    url, 
                                    data=body, 
                                    headers=headers,
                                    allow_redirects=follow_redirects
                                ) as response:
                                    data, content_type = await handle_response(response, success_codes)
                                    
                        elif method == "DELETE":
                            async with session.delete(
                                url, 
                                headers=headers,
                                allow_redirects=follow_redirects
                            ) as response:
                                data, content_type = await handle_response(response, success_codes)
                                
                        elif method == "PATCH":
                            if encode_json:
                                async with session.patch(
                                    url, 
                                    json=body, 
                                    headers=headers,
                                    allow_redirects=follow_redirects
                                ) as response:
                                    data, content_type = await handle_response(response, success_codes)
                            else:
                                async with session.patch(
                                    url, 
                                    data=body, 
                                    headers=headers,
                                    allow_redirects=follow_redirects
                                ) as response:
                                    data, content_type = await handle_response(response, success_codes)
                                    
                        elif method == "HEAD":
                            async with session.head(
                                url, 
                                headers=headers,
                                allow_redirects=follow_redirects
                            ) as response:
                                data, content_type = await handle_response(response, success_codes, head_request=True)
                                
                        else:
                            raise ValueError(f"不支持的HTTP方法: {method}")
                    
                    # 成功跳出重试循环
                    break
                    
                except Exception as e:
                    last_error = e
                    print(f"[CustomAPI]第{attempt + 1}次请求失败: {e}")
                    
                    # 如果不是最后一次尝试，等待一段时间再重试
                    if attempt < max_retries:
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # 指数退避
                    else:
                        # 所有重试都失败
                        error_msg = api.get("error_message", f"API调用失败: {str(last_error)}")
                        await actions.send(
                            group_id=event.group_id,
                            message=Manager.Message(Segments.Text(error_msg))
                        )
                        return True
                        
            # 处理响应模板
            result = await process_template(api["response_template"], data, event, actions)
            
            # 发送响应
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(result))
            )
            
        except Exception as e:
            print(f"[CustomAPI]调用失败: {e}")
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"API调用失败: {e}"))
            )
            
        return True
        
    return False

print("[CustomAPI]自定义API插件已加载")