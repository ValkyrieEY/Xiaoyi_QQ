#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CustomAPI WebUI 诊断脚本
用于诊断WebUI无法打开的问题
"""

import os
import sys
import json
import socket
import requests
import webbrowser
from datetime import datetime

def check_port_availability(host, port):
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception as e:
        print(f"端口检查错误: {e}")
        return False

def check_web_response(url):
    """检查Web响应"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code, response.text[:200]
    except Exception as e:
        return None, str(e)

def diagnose_webui():
    """诊断WebUI问题"""
    print("🔍 CustomAPI WebUI 诊断工具")
    print("=" * 50)
    
    # 1. 检查配置文件 - 修正路径到项目根目录
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "custom_api", "system.json")
    print(f"📁 检查配置文件: {config_path}")
    
    if not os.path.exists(config_path):
        print("❌ 配置文件不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ 配置文件加载成功")
        print(f"   端口: {config.get('web_port', 'Unknown')}")
        print(f"   自动打开: {config.get('auto_open_browser', 'Unknown')}")
    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")
        return False
    
    # 2. 检查HTML模板 - 修正路径
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "custom_api", "templates", "index.html")
    print(f"🌐 检查HTML模板: {template_path}")
    
    if not os.path.exists(template_path):
        print("❌ HTML模板不存在")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        print(f"✅ HTML模板存在 ({len(template)} 字符)")
    except Exception as e:
        print(f"❌ HTML模板读取失败: {e}")
    
    # 3. 检查端口状态
    port = config.get('web_port', 8080)
    print(f"🔌 检查端口状态: {port}")
    
    if check_port_availability('localhost', port):
        print(f"✅ 端口 {port} 正在监听")
    else:
        print(f"❌ 端口 {port} 未在监听")
        return False
    
    # 4. 测试HTTP响应
    url = f"http://localhost:{port}"
    print(f"🌍 测试HTTP响应: {url}")
    
    status_code, response = check_web_response(url)
    if status_code:
        print(f"✅ HTTP响应正常 (状态码: {status_code})")
        print(f"   响应预览: {response}...")
    else:
        print(f"❌ HTTP响应失败: {response}")
        return False
    
    # 5. 检查防火墙和网络
    print("🛡️ 网络检查:")
    print("   - 如果使用防火墙，请确保允许端口访问")
    print("   - 如果使用代理，请检查代理设置")
    print("   - 确保没有其他程序占用端口")
    
    # 6. 浏览器测试
    print("🌐 浏览器测试:")
    try:
        webbrowser.open(url)
        print(f"✅ 尝试在默认浏览器中打开: {url}")
        print("   如果浏览器没有打开，请手动访问上述URL")
    except Exception as e:
        print(f"❌ 自动打开浏览器失败: {e}")
        print(f"   请手动在浏览器中访问: {url}")
    
    # 7. 常见问题解决方案
    print("\n🔧 常见问题解决方案:")
    print("1. 重启机器人程序")
    print("2. 检查是否有其他CustomAPI实例运行")
    print("3. 更改端口号（修改system.json中的web_port）")
    print("4. 检查防火墙设置")
    print("5. 尝试使用不同的浏览器")
    print("6. 检查系统代理设置")
    
    return True

def main():
    """主函数"""
    try:
        # 切换到项目根目录
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        
        success = diagnose_webui()
        
        if success:
            print("\n🎉 诊断完成！如果WebUI仍无法打开，请检查上述建议。")
        else:
            print("\n❌ 发现问题，请根据上述信息进行修复。")
            
    except Exception as e:
        print(f"诊断过程中出现错误: {e}")

if __name__ == "__main__":
    main()