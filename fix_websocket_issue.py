#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("小依QQ机器人 - WebSocket问题修复工具")
    print("=" * 50)
    
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print("1. 检测当前环境...")
    
    python_version = sys.version_info
    print(f"   Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    problematic_packages = []
    
    try:
        import gevent_websocket
        problematic_packages.append(("gevent-websocket", gevent_websocket.__version__))
    except ImportError:
        pass
    
    try:
        import bottle_websocket
        problematic_packages.append(("bottle-websocket", "unknown"))
    except ImportError:
        pass
    
    try:
        import websockets
        problematic_packages.append(("websockets", websockets.__version__))
    except ImportError:
        print("   websockets未安装")
    
    if problematic_packages:
        print("   发现可能冲突的包:")
        for pkg, ver in problematic_packages:
            print(f"     - {pkg}: {ver}")
    
    print("\n2. 修复WebSocket冲突...")
    
    websocket_packages = [
        "websockets",
        "gevent-websocket", 
        "bottle-websocket",
        "websocket-client"
    ]
    
    for package in websocket_packages:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "uninstall", package, "-y"
            ], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print(f"   ✓ 已卸载: {package}")
            else:
                print(f"   - 跳过: {package} (未安装)")
        except Exception as e:
            print(f"   ! 卸载 {package} 时出错: {e}")
    
    print("\n3. 重新安装兼容版本...")
    
    compatible_packages = [
        "websockets>=10.0,<11.0",
        "websocket-client>=1.8.0",
        "gevent-websocket>=0.10.1",
    ]
    
    for package in compatible_packages:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--force-reinstall"
            ], capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                print(f"   ✓ 已安装: {package}")
            else:
                print(f"   ✗ 安装失败: {package}")
                print(f"     错误: {result.stderr}")
        except Exception as e:
            print(f"   ! 安装 {package} 时出错: {e}")
    
    print("\n4. 验证修复结果...")
    
    test_imports = [
        ("websockets", "标准WebSocket库"),
        ("websocket", "WebSocket客户端"),
        ("gevent_websocket", "Gevent WebSocket (可选)"),
    ]
    
    success_count = 0
    for module, description in test_imports:
        try:
            __import__(module)
            print(f"   ✓ {description}: 导入成功")
            success_count += 1
        except ImportError as e:
            if "gevent" in module:
                print(f"   - {description}: 跳过 (可选组件)")
            else:
                print(f"   ✗ {description}: 导入失败 - {e}")
    
    print("\n5. 检查项目配置...")
    
    config_files = [
        "config.json",
        "prerequisites/current.json",
        "appsettings.json"
    ]
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"   ✓ 配置文件存在: {config_file}")
        else:
            print(f"   ! 配置文件缺失: {config_file}")
    
    print("\n" + "=" * 50)
    
    if success_count >= 1:
        print("✅ WebSocket问题修复完成！")
        print("\n建议的后续步骤:")
        print("1. 运行: python main.py")
        print("2. 如果仍有问题，检查OneBot服务是否正常运行")
        print("3. 确保配置文件中的连接地址正确")
    else:
        print("❌ WebSocket问题修复失败！")
        print("\n可能的解决方案:")
        print("1. 手动安装: pip install websockets==10.4")
        print("2. 检查网络连接和pip配置")
        print("3. 使用虚拟环境重新部署")
    
    print("\n6. 生成诊断报告...")
    
    report_content = f"""# 简儿QQ机器人环境诊断报告

## 系统信息
- Python版本: {sys.version}
- 工作目录: {os.getcwd()}
- 脚本路径: {__file__}

## 已安装的WebSocket相关包
"""
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "list", "--format=freeze"
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            installed_packages = result.stdout
            websocket_related = [line for line in installed_packages.split('\n') 
                               if any(ws in line.lower() for ws in ['websocket', 'gevent', 'bottle'])]
            
            if websocket_related:
                report_content += "\n".join(f"- {pkg}" for pkg in websocket_related)
            else:
                report_content += "- 未找到WebSocket相关包"
        else:
            report_content += "- 无法获取包列表"
    except:
        report_content += "- 检查包列表时出错"
    
    report_content += f"""

## 配置文件状态
"""
    
    for config_file in config_files:
        status = "存在" if Path(config_file).exists() else "缺失"
        report_content += f"- {config_file}: {status}\n"
    
    try:
        with open("websocket_diagnosis.txt", "w", encoding="utf-8") as f:
            f.write(report_content)
        print("   ✓ 诊断报告已保存: websocket_diagnosis.txt")
    except Exception as e:
        print(f"   ! 保存诊断报告失败: {e}")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断修复过程")
    except Exception as e:
        print(f"\n修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter键退出...")