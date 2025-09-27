#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简儿QQ机器人完整打包脚本
将整个机器人程序打包成单个exe文件，以SetupWizard.pyw作为入口
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import tempfile

def main():
    # 确保在正确的工作目录
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print("简儿QQ机器人完整打包脚本")
    print("=" * 50)
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
        print(f"✓ PyInstaller已安装，版本: {PyInstaller.__version__}")
    except ImportError:
        print("✗ PyInstaller未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller安装完成")
    
    # 安装打包依赖
    if Path("requirements_build.txt").exists():
        print("正在安装打包依赖...")
        try:
            # 尝试先卒载可能冲突的包
            try:
                subprocess.run([sys.executable, "-m", "pip", "uninstall", "websockets", "-y"], 
                             capture_output=True, check=False)
            except:
                pass
            
            # 安装打包依赖
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_build.txt", "--force-reinstall"])
            print("✓ 打包依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"⚠ 部分依赖安装失败: {e}")
            print("将继续打包过程...")            
    
    # 定义文件路径
    setup_wizard_path = "SetupWizard.pyw"
    spec_file_path = "jianer_bot.spec"
    dist_dir = Path("dist")
    build_dir = Path("build")
    
    # 检查主要文件是否存在
    if not Path("launcher.py").exists():
        print(f"✗ 入口文件 launcher.py 不存在！")
        return False
    
    if not Path("main.py").exists():
        print("✗ 主程序文件 main.py 不存在！")
        return False
    
    print("✓ 主要文件检查通过")
    
    # 清理之前的构建文件
    if dist_dir.exists():
        print("清理旧的dist目录...")
        shutil.rmtree(dist_dir)
    
    if build_dir.exists():
        print("清理旧的build目录...")
        shutil.rmtree(build_dir)
    
    if Path(spec_file_path).exists():
        print("清理旧的spec文件...")
        Path(spec_file_path).unlink()
    
    # 创建spec文件内容
    spec_content = create_spec_file()
    
    # 写入spec文件
    with open(spec_file_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✓ 已创建 {spec_file_path}")
    
    # 执行打包
    print("开始打包...")
    try:
        cmd = [sys.executable, "-m", "PyInstaller", spec_file_path, "--clean", "--noconfirm"]
        subprocess.check_call(cmd)
        print("✓ 打包完成！")
    except subprocess.CalledProcessError as e:
        print(f"✗ 打包失败: {e}")
        return False
    
    # 检查输出文件
    exe_path = dist_dir / "JianerBot.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ 生成的可执行文件: {exe_path}")
        print(f"✓ 文件大小: {size_mb:.1f} MB")
        
        # 创建运行说明
        create_readme()
        
        print("\n" + "=" * 50)
        print("打包成功！")
        print(f"可执行文件位置: {exe_path.absolute()}")
        print("请查看同目录下的 运行说明.txt 了解使用方法")
        print("=" * 50)
        return True
    else:
        print("✗ 未找到生成的可执行文件")
        return False

def create_spec_file():
    """创建PyInstaller spec文件"""
    return '''# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 获取项目根目录
project_root = Path(SPECPATH)

# 分析主程序和所有依赖
a = Analysis(
    ['launcher.py'],  # 入口文件
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # 配置文件和数据目录
        ('config', 'config'),
        ('data', 'data'),
        ('lgr', 'lgr'),
        ('assets', 'assets'),
        ('prerequisites', 'prerequisites'),
        
        # UI相关文件
        ('wizardWindows', 'wizardWindows'),
        ('wizardTools', 'wizardTools'),
        ('UI', 'UI'),
        
        # 核心模块
        ('Tools', 'Tools'),
        ('plugins', 'plugins'),
        ('ai_plugins', 'ai_plugins'),
        
        # 主程序文件
        ('main.py', '.'),
        ('launcher.py', '.'),
        ('SetupWizard.pyw', '.'),
        ('WizardUIs.py', '.'),
        
        # 配置文件
        ('requirements.txt', '.'),
        ('*.json', '.'),
        ('*.ini', '.'),
        ('*.md', '.'),
    ],
    hiddenimports=[
        # 核心依赖
        'PySide6',
        'qfluentwidgets',
        'openai',
        'google.generativeai',
        'edge_tts',
        'paramiko',
        'requests',
        'aiohttp',
        'asyncio',
        'threading',
        'subprocess',
        'pathlib',
        'json',
        'os',
        'sys',
        'datetime',
        'time',
        'traceback',
        'uuid',
        'random',
        'hashlib',
        'base64',
        'urllib.parse',
        'urllib.request',
        'tempfile',
        'shutil',
        'webbrowser',
        'io',
        'emoji',
        
        # 项目模块
        'Tools.tools',
        'Tools.GoogleAI',
        'Tools.SearchOnline',
        'Tools.deepseek',
        'Tools.workflow_manager',
        'Tools.group_notice_manager',
        'Tools.AI_tools',
        
        # AI插件系统
        'ai_plugins',
        'ai_plugins.ai_plugin_manager',
        'ai_plugins.base_ai_plugin',
        'ai_plugins.memory_manager',
        
        # UI相关
        'WizardUIs',
        'wizardTools.PluginsManager',
        'wizardTools.PresetsValidate',
        'wizardTools.GithubTools',
        'wizardTools.TaskRunner',
        
        # 预设系统
        'prerequisites.prerequisite',
        
        # PySide6相关
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtNetwork',
        
        # qfluentwidgets相关
        'qfluentwidgets.components',
        'qfluentwidgets.common',
        'qfluentwidgets.window',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小体积
        'tkinter',
        'matplotlib',
        'scipy',
        'numpy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'pytest',
        'setuptools',
        'pip',
        'wheel',
        'pyppeteer',  # 可能导致冲突的模块
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# 移除重复的二进制文件
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# 创建单文件可执行程序
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JianerBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用UPX以避免兼容性问题
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='wizardWindows/Icon_rounded.png' if os.path.exists('wizardWindows/Icon_rounded.png') else None,
)
'''

def create_readme():
    """创建运行说明文件"""
    readme_content = '''简儿QQ机器人 - 运行说明
============================

这是简儿QQ机器人的完整打包版本，包含了配置向导和机器人主程序。

## 使用方法

1. 双击 JianerBot.exe 启动配置向导
2. 在配置向导中设置机器人的基本信息、AI密钥等
3. 配置完成后可以直接在向导中启动机器人
4. 也可以通过命令行运行机器人：JianerBot.exe --run-bot

## 主要功能

- 图形化配置向导
- AI对话支持（ChatGPT、DeepSeek、Gemini）
- 插件系统
- 工作流自动化
- 群管功能
- 语音回复（TTS）

## 系统要求

- Windows 10/11 (64位)
- 网络连接（用于AI服务和插件下载）
- OneBot协议兼容的QQ客户端（如go-cqhttp、Lagrange等）

## 注意事项

1. 首次运行请确保网络畅通，用于下载必要的资源
2. 使用AI功能需要配置相应的API密钥
3. 部分功能可能需要管理员权限
4. 建议在防火墙中允许程序联网

## 故障排除

如果遇到问题，请：
1. 检查网络连接
2. 确认OneBot服务端正常运行
3. 查看程序日志文件
4. 联系开发者获取支持

## 开发者信息

- 项目：简儿QQ机器人 Jianer NEXT 3
- 开发：思锐工作室
- 版本：3.0 - Next Preview Ultra
- 官网：https://www.sr-studio.cn/

============================
感谢使用简儿QQ机器人！
'''
    
    with open('运行说明.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    try:
        success = main()
        if success:
            input("\n按Enter键退出...")
        else:
            input("\n打包失败，按Enter键退出...")
    except KeyboardInterrupt:
        print("\n用户中断打包过程")
    except Exception as e:
        print(f"\n打包过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter键退出...")