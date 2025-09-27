#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("小依DEMO")
    print("=" * 50)
    
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print("1. 清理旧的构建文件...")
    cleanup_files = ["jianer_bot.spec", "dist", "build", "__pycache__"]
    for item in cleanup_files:
        item_path = Path(item)
        if item_path.exists():
            if item_path.is_dir():
                import shutil
                shutil.rmtree(item_path)
                print(f"   已删除目录: {item}")
            else:
                item_path.unlink()
                print(f"   已删除文件: {item}")
    
    print("\n2. 修复依赖冲突...")
    
    conflicting_packages = ["websockets", "pyppeteer"]
    for package in conflicting_packages:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "uninstall", package, "-y"
            ], capture_output=True, check=False)
            print(f"   已卸载可能冲突的包: {package}")
        except:
            pass
    
    print("\n3. 重新安装正确版本的依赖...")
    
    key_dependencies = [
        "hyper-bot==0.78.2",
        "websockets>=10.0,<11.0",
        "PySide6>=6.5.0",
        "PySide6-Fluent-Widgets>=1.4.0",
        "PyInstaller>=5.0",
        "requests>=2.28.0",
        "openai>=1.35.12",
        "google-generativeai==0.7.2",
        "edge-tts>=6.1.0",
        "paramiko>=3.5.1",
    ]
    
    for dep in key_dependencies:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep, "--force-reinstall"
            ])
            print(f"   ✓ 已安装: {dep}")
        except subprocess.CalledProcessError as e:
            print(f"   ✗ 安装失败: {dep} - {e}")
    
    print("\n4. 检查关键模块...")
    
    test_imports = [
        ("PySide6", "PySide6 GUI框架"),
        ("qfluentwidgets", "FluentWidgets组件库"),
        ("openai", "OpenAI SDK"),
        ("edge_tts", "Edge TTS语音合成"),
        ("requests", "HTTP请求库"),
    ]
    
    for module, description in test_imports:
        try:
            __import__(module)
            print(f"   ✓ {description}: 正常")
        except ImportError as e:
            print(f"   ✗ {description}: 导入失败 - {e}")
    
    print("\n5. 检查项目文件...")
    
    required_files = [
        "launcher.py",
        "SetupWizard.pyw", 
        "main.py",
        "WizardUIs.py",
        "Tools",
        "plugins",
        "ai_plugins",
        "wizardWindows",
        "config",
        "data",
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            print(f"   ✗ 缺少: {file_path}")
        else:
            print(f"   ✓ 存在: {file_path}")
    
    print("\n6. 生成修复建议...")
    
    if missing_files:
        print(f"   ⚠ 发现缺少文件: {', '.join(missing_files)}")
        print("   请确保所有必要文件都存在后再进行打包")
    else:
        print("   ✓ 所有必要文件都存在")
    
    print("\n修复完成！建议的后续步骤：")
    print("1. 运行: python build_jianer.py")
    print("2. 如果仍有问题，尝试: python -m PyInstaller --onefile --windowed launcher.py")
    print("3. 检查生成的 dist 目录中的可执行文件")
    
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