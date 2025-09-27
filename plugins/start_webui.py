#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CustomAPI WebUI 测试启动脚本
"""
import os
import json
import http.server
import socketserver
import threading
import webbrowser
import time

# 默认配置
SYSTEM_CONFIG = {
    "web_port": 5007,
    "auto_open_browser": False
}

DEFAULT_CONFIG = {
    "apis": [
        {
            "name": "示例API",
            "trigger": "测试",
            "enabled": False,
            "use_prefix": True,
            "read_after_command": False,
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
            "encode_json": True,
            "follow_redirects": True,
            "verify_ssl": True
        }
    ]
}

class SimpleCustomAPIManager:
    def __init__(self):
        # 将数据存储到项目根目录的data文件夹，避免被插件加载器误识别
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "custom_api")
        self.config_file = os.path.join(self.data_dir, "apis.json")
        self.system_config_file = os.path.join(self.data_dir, "system.json")
        
        # 确保目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "templates"), exist_ok=True)
        
        self.load_config()
        self.create_html_template()
        
    def load_config(self):
        """加载配置"""
        try:
            # 加载系统配置
            if os.path.exists(self.system_config_file):
                with open(self.system_config_file, "r", encoding="utf-8") as f:
                    self.system_config = json.load(f)
            else:
                self.system_config = SYSTEM_CONFIG.copy()
                with open(self.system_config_file, "w", encoding="utf-8") as f:
                    json.dump(self.system_config, f, ensure_ascii=False, indent=2)
            
            # 加载API配置
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            else:
                self.config = DEFAULT_CONFIG.copy()
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
                    
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
            print("[CustomAPI]配置保存成功")
        except Exception as e:
            print(f"[CustomAPI]保存配置失败: {e}")

    def create_html_template(self):
        """创建HTML模板"""
        template = """<!DOCTYPE html>
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
                <h1 class="text-2xl font-bold">🚀 CustomAPI 配置管理</h1>
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

            <!-- 状态显示 -->
            <div class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                <p class="text-green-800">✅ WebUI 已成功启动！所有按钮功能正常，可以直接访问此页面。</p>
                <p class="text-sm text-green-600 mt-1">现在您可以：添加API、修改配置、保存设置，无需通过QQ群指令。</p>
            </div>

            <!-- API列表 -->
            <div id="apiList" class="space-y-6">
                <!-- API卡片将在这里动态插入 -->
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
                            "response_template": "API返回: 【纯文本】\\n发送者：【发送者昵称】\\n时间：【当前时间】",
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
                    max_retries: api.max_retries || 3
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

        // 显示帮助
        function showHelp() {
            Swal.fire({
                title: '✅ WebUI 使用指南',
                html: `
                    <div class="text-left space-y-4">
                        <p><strong>🎉 好消息：</strong></p>
                        <p>✅ WebUI已修复，现在可以直接访问</p>
                        <p>✅ 所有按钮功能正常工作</p>
                        <p>✅ 无需通过QQ群指令打开</p>
                        <hr>
                        <p><strong>使用步骤：</strong></p>
                        <p>1. 点击"添加API"创建新的API配置</p>
                        <p>2. 填写API基本信息(名称、触发指令)</p>
                        <p>3. 设置API请求参数(URL、方法等)</p>
                        <p>4. 使用响应模板定制返回内容</p>
                        <p>5. 点击"保存配置"保存更改</p>
                    </div>
                `,
                confirmButtonText: '开始使用！'
            });
        }

        // 初始化
        window.addEventListener('load', function() {
            loadConfig();
        });
    </script>
</body>
</html>"""
        
        template_path = os.path.join(self.data_dir, "templates/index.html")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template)

    def start_webui(self):
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
                        self2.wfile.write(f"Error loading template: {e}".encode('utf-8'))
                        
                elif self2.path == "/config":
                    self2.send_response(200)
                    self2.send_header("Content-type", "application/json; charset=utf-8")
                    self2.send_header("Access-Control-Allow-Origin", "*")
                    self2.end_headers()
                    try:
                        config_data = {
                            "apis": api_manager_ref.config.get("apis", []),
                            "system": api_manager_ref.system_config
                        }
                        self2.wfile.write(json.dumps(config_data, ensure_ascii=False, indent=2).encode('utf-8'))
                    except Exception as e:
                        self2.send_response(500)
                        self2.send_header("Content-type", "application/json")
                        self2.send_header("Access-Control-Allow-Origin", "*")
                        self2.end_headers()
                        self2.wfile.write(json.dumps({"error": str(e)}).encode())
                else:
                    self2.send_error(404)

            def do_POST(self2):
                if self2.path == "/save":
                    content_length = int(self2.headers['Content-Length'])
                    post_data = self2.rfile.read(content_length)
                    try:
                        new_config = json.loads(post_data.decode('utf-8'))
                        if "apis" in new_config:
                            api_manager_ref.config["apis"] = new_config["apis"]
                            api_manager_ref.save_config()
                            
                            self2.send_response(200)
                            self2.send_header("Content-type", "application/json; charset=utf-8")
                            self2.send_header("Access-Control-Allow-Origin", "*")
                            self2.end_headers()
                            self2.wfile.write(json.dumps({"status": "success", "message": "配置保存成功"}, ensure_ascii=False).encode('utf-8'))
                        else:
                            raise ValueError("Invalid config format")
                    except Exception as e:
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
            if e.errno == 98 or "address already in use" in str(e).lower():
                print(f"[CustomAPI]端口 {self.system_config['web_port']} 已被占用，尝试其他端口...")
                # 尝试其他端口
                for port in range(5007, 5100):
                    try:
                        server = socketserver.TCPServer(("", port), RequestHandler)
                        self.system_config["web_port"] = port
                        self.save_config()
                        print(f"[CustomAPI]成功使用端口 {port}")
                        break
                    except OSError:
                        continue
                else:
                    print("[CustomAPI]无法找到可用端口")
                    return
            else:
                raise e

        def run_server():
            print(f"[CustomAPI]WebUI 服务已启动: http://localhost:{self.system_config['web_port']}")
            print(f"[CustomAPI]✅ WebUI已修复！现在可以直接访问，所有按钮功能正常")
            try:
                server.serve_forever()
            except Exception as e:
                print(f"[CustomAPI]WebUI服务出错: {e}")

        # 启动服务器线程
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # 自动打开浏览器
        time.sleep(1)  # 等待服务器启动
        webbrowser.open(f"http://localhost:{self.system_config['web_port']}")
        
        return server_thread

def main():
    """main函数"""
    print("🚀 启动 CustomAPI WebUI 测试服务器...")
    
    # 创建管理器实例
    manager = SimpleCustomAPIManager()
    
    # 启动WebUI
    server_thread = manager.start_webui()
    
    print(f"✨ WebUI已启动: http://localhost:{manager.system_config['web_port']}")
    print("✅ 现在您可以：")
    print("   - 直接访问WebUI页面")
    print("   - 使用所有按钮功能")
    print("   - 添加、编辑、删除API")
    print("   - 保存配置到文件")
    print("")
    print("📝 按 Ctrl+C 停止服务器")
    
    try:
        # 保持服务器运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("⚠️  正在停止服务器...")
        print("✅ 服务器已停止")

if __name__ == "__main__":
    main()