#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

def main():
    import datetime
    log_file = "launcher_debug.log"
    
    def log_message(msg):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] {msg}\n")
        print(msg)
    
    log_message("启动器开始运行...")
    
    if hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
        exe_dir = Path(sys.executable).parent
        os.chdir(exe_dir)
        log_message(f"打包环境 - 临时目录: {base_path}, 工作目录: {exe_dir}")
        
        import prerequisites.prerequisite as prereq_module
        prereq_module.CONFIG_FILE = str(base_path / "prerequisites" / "current.json")
        prereq_module.PRESET_DIR = str(base_path / "prerequisites")
        log_message(f"修复配置文件路径: {prereq_module.CONFIG_FILE}")
        
    else:
        base_path = Path(__file__).parent
        os.chdir(base_path)
        log_message(f"开发环境 - 工作目录: {base_path}")
    
    if str(base_path) not in sys.path:
        sys.path.insert(0, str(base_path))
        log_message(f"添加基础路径到sys.path: {base_path}")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--run-bot' or sys.argv[1] == '--main':
            print("正在启动简儿QQ机器人主程序...")
            try:
                import main
            except Exception as e:
                print(f"启动机器人失败: {e}")
                input("按Enter键退出...")
                sys.exit(1)
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("""
简儿QQ机器人启动器

用法:
  JianerBot.exe              启动配置向导（默认）
  JianerBot.exe --run-bot    直接运行机器人主程序
  JianerBot.exe --main       直接运行机器人主程序
  JianerBot.exe --help       显示此帮助信息

配置向导功能:
  - 图形化配置机器人参数
  - AI密钥管理
  - 插件管理
  - 工作流配置
  - 实时日志查看
  - 一键启动机器人
            """)
            input("按Enter键退出...")
            return
        else:
            print(f"未知参数: {sys.argv[1]}")
            print("使用 --help 查看帮助信息")
            input("按Enter键退出...")
            return
    
    log_message("正在启动简儿QQ机器人配置向导...")
    try:
        log_message("尝试导入 SetupWizard 模块...")
        import SetupWizard
        log_message("SetupWizard 模块导入成功")
        log_message("配置向导应该已经启动")
    except Exception as e:
        log_message(f"启动配置向导失败: {e}")
        import traceback
        error_msg = traceback.format_exc()
        log_message(f"详细错误信息:\n{error_msg}")
        
        print(f"启动失败: {e}")
        print(f"请查看 {log_file} 获取详细信息")
        input("按Enter键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()