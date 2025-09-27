import os
import sys
import time
import configparser
import psutil
from pathlib import Path
import logging

class ProcessGuard:
    def __init__(self):
        self.config_file = "guard_config.ini"
        self.script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        self.restart_interval = 0  # 0表示不自动重启
        self.process = None
        self.setup_logger()
        self.load_config()

    def setup_logger(self):
        self.logger = logging.getLogger("ProcessGuard")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("process_guard.log", encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.info("Logger initialized.")

    def load_config(self):
        """加载配置文件（ini格式）"""
        config = configparser.ConfigParser()
        if not os.path.exists(self.config_file):
            self.logger.info(f"配置文件 {self.config_file} 不存在，自动创建默认配置。")
            self.save_config()
            return
        try:
            config.read(self.config_file, encoding="utf-8")
            if 'Guard' in config:
                self.script_path = config['Guard'].get('script_path', self.script_path)
                self.restart_interval = config['Guard'].getint('restart_interval', 0)
            self.logger.info(f"配置文件加载成功: script_path={self.script_path}, restart_interval={self.restart_interval}")
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            print(f"加载配置文件失败: {e}")

    def save_config(self):
        """保存配置到ini文件"""
        config = configparser.ConfigParser()
        config['Guard'] = {
            'script_path': self.script_path,
            'restart_interval': str(self.restart_interval)
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)
            self.logger.info(f"配置文件已保存: script_path={self.script_path}, restart_interval={self.restart_interval}")
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}")
            print(f"保存配置文件失败: {e}")
    
    def set_restart_interval(self):
        """设置自动重启间隔"""
        try:
            interval = input("请输入自动重启间隔（秒，0表示不自动重启）: ")
            self.restart_interval = int(interval)
            self.save_config()
            self.print_with_time(f"重启间隔已设置为 {self.restart_interval} 秒")
            self.logger.info(f"用户设置重启间隔为 {self.restart_interval} 秒")
        except ValueError:
            self.print_with_time("输入无效，请输入数字！")
            self.logger.warning("用户输入了无效的重启间隔。")

    def is_process_running(self):
        """检查进程是否在运行"""
        if self.process is None:
            return False
        try:
            running = self.process.is_running() and self.process.status() != psutil.STATUS_ZOMBIE
            self.logger.debug(f"检查进程状态: PID={self.process.pid}, running={running}")
            return running
        except psutil.NoSuchProcess:
            self.logger.warning("检测到进程不存在。")
            return False

    def start_process(self):
        """启动Python脚本进程（新控制台窗口）"""
        try:
            import subprocess
            if not os.path.exists(self.script_path):
                self.print_with_time("脚本文件不存在！")
                self.logger.error(f"脚本文件不存在: {self.script_path}")
                return False
            
            python_executable = sys.executable
            process = subprocess.Popen(
                [python_executable, self.script_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.process = psutil.Process(process.pid)
            self.print_with_time(f"脚本已在新控制台启动，PID: {self.process.pid}")
            self.logger.info(f"脚本已启动，PID: {self.process.pid}")
            return True
        except Exception as e:
            self.print_with_time(f"启动脚本失败: {e}")
            self.logger.error(f"启动脚本失败: {e}")
            return False

    def stop_process(self):
        """停止进程"""
        if self.process:
            try:
                self.logger.info(f"尝试终止进程 PID: {self.process.pid}")
                self.process.terminate()
                self.process.wait(timeout=3)
                self.print_with_time(f"进程 PID: {self.process.pid} 已正常终止")
                self.logger.info(f"进程 PID: {self.process.pid} 已正常终止")
            except psutil.NoSuchProcess:
                self.print_with_time("进程不存在，无法终止。")
                self.logger.warning("进程不存在，无法终止。")
            except psutil.TimeoutExpired:
                self.print_with_time("进程未及时结束，尝试强制杀死。")
                self.logger.warning("进程未及时结束，尝试强制杀死。")
                self.process.kill()
                self.print_with_time(f"进程 PID: {self.process.pid} 已被强制杀死")
                self.logger.info(f"进程 PID: {self.process.pid} 已被强制杀死")
            self.process = None

    def print_with_time(self, msg):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}] {msg}")

    def start_guard(self):
        """开始守护进程"""
        if not self.script_path:
            self.print_with_time("请先选择Python脚本！")
            self.logger.error("未设置脚本路径，无法守护。");
            return

        self.print_with_time("开始守护进程...")
        self.logger.info("守护进程启动。")
        counter = 0
        last_running = False

        try:
            while True:
                running = self.is_process_running()
                if not running:
                    if last_running:
                        self.print_with_time("检测到程序崩溃，正在重新启动...")
                        self.logger.warning("检测到程序崩溃，正在重新启动...")
                    else:
                        self.print_with_time("检测到进程未运行，尝试启动。")
                        self.logger.info("检测到进程未运行，尝试启动。")
                    self.start_process()
                    last_running = False
                else:
                    last_running = True
                time.sleep(1)
                if self.restart_interval > 0 and self.is_process_running():
                    counter += 1
                    if counter >= self.restart_interval:
                        self.print_with_time("执行定时重启...")
                        self.logger.info("达到定时重启间隔，重启进程。")
                        self.stop_process()
                        counter = 0
        except KeyboardInterrupt:
            self.print_with_time("\n停止守护进程...")
            self.logger.info("用户中断，守护进程停止。")
            self.stop_process()

    def set_script_path(self):
        """手动设置需要守护的脚本路径"""
        path = input("请输入需要守护的脚本完整路径（如 D:\\xxx\\main.py）: ").strip()
        if not os.path.isfile(path):
            self.print_with_time("文件不存在，请检查路径！")
            self.logger.warning(f"用户输入的脚本路径不存在: {path}")
            return
        self.script_path = path
        self.save_config()
        self.print_with_time(f"脚本路径已设置为: {self.script_path}")
        self.logger.info(f"用户设置脚本路径为: {self.script_path}")

def main():
    guard = ProcessGuard()
    
    while True:
        print("\n=== 小依脚本守护程序 ===")
        print("Developed by: 小依")
        print("Version: 1.0")
        print("免费程序，开源博客xun.eynet.top")
        print(f"========================")
        print(f"当前脚本路径: {guard.script_path}")
        print(f"========================")
        print("1. 设置自动重启时间")
        print("2. 开始守护")
        print("3. 设置脚本路径")
        print("4. 退出")
        
        try:
            choice = input("请选择操作: ")
            if choice == '1':
                guard.set_restart_interval()
            elif choice == '2':
                guard.start_guard()
            elif choice == '3':
                guard.set_script_path()
            elif choice == '4':
                confirm = input("确认要退出吗？(y/n): ")
                if confirm.lower() == 'y':
                    print("程序已退出")
                    guard.logger.info("用户退出程序。")
                    break
            else:
                print("无效的选择！")
                guard.logger.warning("用户做出了无效的选择。")
        except KeyboardInterrupt:
            print("\n程序已退出")
            guard.logger.info("程序被中断。")
            break

if __name__ == '__main__':
    main()
