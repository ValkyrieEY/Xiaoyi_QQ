import json
import random
import shutil
import subprocess, tempfile
import traceback
import hashlib
from typing import Optional
from pathlib import Path
from PySide6.QtCore import Qt, QSize, QCoreApplication, QThread, QTimer, Slot, QThreadPool, QMetaObject, Q_ARG, QRunnable, Signal, QProcess
from PySide6.QtGui import QIcon, QColor, QTextCursor
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QTextEdit, QSplitter
import sys, os, edge_tts, asyncio
import webbrowser
from urllib.request import getproxies
import io
import datetime

from qfluentwidgets import (SplitFluentWindow, FluentIcon, 
                            NavigationItemPosition, CardWidget, LineEdit, PrimaryPushButton, PushButton, SubtitleLabel, 
                            FluentTranslator, Theme, setTheme, setThemeColor, isDarkTheme, InfoBar, InfoBarPosition, 
                            SplashScreen, MessageBox, TitleLabel, StrongBodyLabel, StateToolTip)

from PySide6 import QtCore, QtGui, QtWidgets

# 启动子类
from WizardUIs import *
import prerequisites.prerequisite as presets_tool
from wizardTools.PresetsValidate import *
from wizardTools import PluginsManager
from wizardTools.GithubTools import *
from wizardTools.TaskRunner import TaskRunner
import traceback

# 统一全局工作目录
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 初始化预设
presets = presets_tool.read_presets()
presets_page_tip_showed = False

# 配置文件内容
config_content = ""
appSettings_content = ""
presets_content = ""

# 预设内容
preset_layout = []

# TTS音色数据
voices = None

# 插件相关
plugins_num = 0 # 已加载的插件数量
plugins_list = {} # 全部插件
local_plugins_list = [] 
updatable_plugin_list = []
plugin_installing = False #是否正在安装插件

# 继承 QApplication
class Application(QApplication):
    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except Exception as e:
            print(f"Unhandled exception: {e}")
            QMessageBox.critical(None, "Error", f"An unhandled exception occurred: {e}")
            return True

# 机器人进程管理器
class BotProcessManager(QProcess):
    # 定义信号
    outputReceived = Signal(str)  # 输出信号
    errorReceived = Signal(str)   # 错误信号
    processFinished = Signal(int) # 进程结束信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.finished.connect(self.processFinished)
        self.readyReadStandardOutput.connect(self._readStandardOutput)
        self.readyReadStandardError.connect(self._readStandardError)
        
        # 设置进程参数以确保能够捕获输出
        self.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        # 设置环境变量确保Python输出不被缓冲
        env = self.processEnvironment()
        env.insert("PYTHONUNBUFFERED", "1")
        env.insert("PYTHONIOENCODING", "utf-8")
        self.setProcessEnvironment(env)
    
    def _readStandardOutput(self):
        """读取标准输出"""
        try:
            data = self.readAllStandardOutput().data()
            if data:
                # 尝试多种编码方式
                text = ""
                for encoding in ['utf-8', 'gbk', 'gb2312', 'ascii']:
                    try:
                        text = data.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if text:
                    self.outputReceived.emit(text)
                elif data:  # 如果所有编码都失败，使用错误忽略模式
                    text = data.decode('utf-8', errors='ignore')
                    self.outputReceived.emit(text)
        except Exception as e:
            self.errorReceived.emit(f"读取输出时发生错误: {str(e)}")
    
    def _readStandardError(self):
        """读取标准错误"""
        try:
            data = self.readAllStandardError().data()
            if data:
                # 尝试多种编码方式
                text = ""
                for encoding in ['utf-8', 'gbk', 'gb2312', 'ascii']:
                    try:
                        text = data.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if text:
                    self.errorReceived.emit(text)
                elif data:  # 如果所有编码都失败，使用错误忽略模式
                    text = data.decode('utf-8', errors='ignore')
                    self.errorReceived.emit(text)
        except Exception as e:
            self.errorReceived.emit(f"读取错误输出时发生错误: {str(e)}")
    
    def start_bot(self, python_path="python", main_script="main.py"):
        """启动机器人"""
        try:
            # 设置工作目录
            self.setWorkingDirectory(os.getcwd())
            # 使用-u参数确保Python输出不被缓冲
            args = ["-u", main_script]
            # 启动进程
            self.start(python_path, args)
            return True
        except Exception as e:
            self.errorReceived.emit(f"启动失败: {str(e)}")
            return False
    
    def stop_bot(self):
        """停止机器人"""
        if self.state() == QProcess.ProcessState.Running:
            self.terminate()
            # 如果5秒内没有终止，强制杀死
            if not self.waitForFinished(5000):
                self.kill()
                self.waitForFinished(3000) 

class SetupWizard(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("小依 OneBot")
        self.setWindowIcon(QIcon(os.path.abspath('.//wizardWindows/icon.png')))
        self.resize(1000, 700)
        
        # 1. 创建启动页面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))

        # 2. 在创建其他子页面前先显示主界面
        self.show()

        # 实例化所有页面
        self.intelliMarkets = None
        self.jianer_setup_wizard = JianerSetupWizard(self)
        self.jianer_setup_wizard.setObjectName("JianerSetupWizard")
        self.jianer_setup_basic = JianerSetupBasic(self)
        self.jianer_setup_basic.setObjectName("JianerSetupBasic")
        self.jianer_setup_ai = JianerSetupAI(self)
        self.jianer_setup_ai.setObjectName("JianerSetupAI")
        self.jianer_setup_pre = JianerSetupPre(self)
        self.jianer_setup_pre.setObjectName("JianerSetupPre")
        self.jianer_setup_lgr = JianerSetupLgr(self)
        self.jianer_setup_lgr.setObjectName("JianerSetupLgr")
        self.jianer_setup_advanced = JianerSetupAdvanced(self)
        self.jianer_setup_advanced.setObjectName("JianerSetupAdvanced")
        self.jianer_setup_apply = JianerSetupApply(self)
        self.jianer_setup_apply.setObjectName("JianerSetupApply")
        self.jianer_setup_about = JianerSetupAbout(self)
        self.jianer_setup_about.setObjectName("JianerSetupAbout")
        self.jianer_setup_others = JianerSetupOthers(self)
        self.jianer_setup_others.setObjectName("JianerSetupOthers")
        self.jianer_setup_TTS = JianerSetupTTS(self)
        self.jianer_setup_TTS.setObjectName("JianerSetupTTS")
        self.jianer_setup_plugins = JianerSetupPlugins(self)
        self.jianer_setup_plugins.setObjectName("JianerSetupPlugins")
        self.jianer_setup_workflow = JianerSetupWorkflow(self)
        self.jianer_setup_workflow.setObjectName("JianerSetupWorkflow")
        
        # 自适应关于页面的图标颜色 - 已禁用，因为关于页面改为版本介绍卡片
        if isDarkTheme():
            self.jianer_setup_wizard.line.setStyleSheet("color: rgb(255, 255, 255);")
            # 原图标设置代码已删除，因为关于页面不再使用按钮
        else:
            self.jianer_setup_wizard.line.setStyleSheet("color: rgb(0.0.0.0);")
            # 原图标设置代码已删除，因为关于页面不再使用按钮
        
        # 定义 jianer_setup_pre 中所有按钮的点击事件
        self.jianer_setup_pre.PrimaryPushButton_2.clicked.connect(lambda: self.new_preset(None, "标题", "介绍", "", True))

        # 定义 jianer_setup_pre 中的可选选项（速率，音量，音调）
        asyncio.run(self.load_pre_voices())
        times = -100
        for i in range(21):
            i_index = ""
            if times >= 0:
                i_index = f"+{times}"
            else:
                i_index = f"{times}"
                
            self.jianer_setup_TTS.ttsRate.addItem(f"{i_index}%")
            self.jianer_setup_TTS.ttsVolume.addItem(f"{i_index}%")
            self.jianer_setup_TTS.ttsPitCh.addItem(f"{i_index}Hz")
            times += 10
        
        # 定义 jianer_setup_wizard 中所有按钮的点击事件
        self.jianer_setup_wizard.NormalIconButton.clicked.connect(lambda: self.switchTo(self.jianer_setup_basic))
        self.jianer_setup_wizard.NormalIconButton_2.clicked.connect(lambda: self.switchTo(self.jianer_setup_ai))
        self.jianer_setup_wizard.NormalIconButton_4.clicked.connect(lambda: self.switchTo(self.jianer_setup_pre))
        self.jianer_setup_wizard.NormalIconButton_3.clicked.connect(lambda: self.switchTo(self.jianer_setup_lgr))
        self.jianer_setup_wizard.NormalIconButton_5.clicked.connect(lambda: self.switchTo(self.jianer_setup_advanced))
        self.jianer_setup_wizard.PluginIconButton.clicked.connect(lambda: self.switchTo(self.jianer_setup_plugins))
        self.jianer_setup_wizard.OtherIconButton.clicked.connect(lambda: self.switchTo(self.jianer_setup_others))
        
        # 添加工作流按钮
        self.add_workflow_button()
        
        # 定义 jianer_setup_about 中所有按钮的点击事件 - 已禁用，因为关于页面改为版本介绍卡片
        # 原按钮点击事件已删除，因为关于页面不再使用可点击按钮
        
        # 定义 jianer_setup_plugins 中的按钮
        self.jianer_setup_plugins.SearchButton.setIcon(FluentIcon.SEARCH)
        self.jianer_setup_plugins.marketButton.clicked.connect(lambda: webbrowser.open("https://github.com/IntelliMarkets/Jianer_Plugins_Index"))
        self.jianer_setup_plugins.wikiButton.clicked.connect(lambda: webbrowser.open("https://github.com/SRInternet-Studio/Jianer_QQ_bot/wiki/Create-a-New-Plugin/"))
        
        # 定义 jianer_setup_plugins 中的选项
        self.jianer_setup_plugins.ComboBox.clear()
        self.jianer_setup_plugins.ComboBox.addItem("筛选：全部")
        self.jianer_setup_plugins.ComboBox.addItem("筛选：已安装")
        self.jianer_setup_plugins.ComboBox.addItem("筛选：可更新")
        self.jianer_setup_plugins.ComboBox.setCurrentIndex(0)
        self.jianer_setup_plugins.ComboBox.currentIndexChanged.connect(lambda: self.update_plain_plugins())
        self.jianer_setup_plugins.SearchBox.returnPressed.connect(lambda: self.search_plain_plugins(self.jianer_setup_plugins.SearchBox.text()))
        self.jianer_setup_plugins.SearchButton.clicked.connect(lambda: self.search_plain_plugins(self.jianer_setup_plugins.SearchBox.text()))

        # 定义 jianer_setup_advanced 中的可选代理
        self.jianer_setup_advanced.SplitPushButton.clear()
        self.jianer_setup_advanced.SplitPushButton.addItem("Master - cloudflare")
        self.jianer_setup_advanced.SplitPushButton.addItem("Master - mainland")
        self.jianer_setup_advanced.SplitPushButton.addItem("Mirror - hk > cloudflare")
        self.jianer_setup_advanced.SplitPushButton.setCurrentIndex(0)
        
        # 定义 jianer_setup_ai 中的可选代理
        self.jianer_setup_ai.ComboBox.clear()
        self.jianer_setup_ai.ComboBox.addItem("DeepSeek (深度)")
        self.jianer_setup_ai.ComboBox.addItem("Google Gemini (读图)")
        self.jianer_setup_ai.ComboBox.addItem("ChatGPT-4 (默认4)")
        self.jianer_setup_ai.ComboBox.addItem("ChatGPT-3.5 (默认3.5)")
        self.jianer_setup_ai.ComboBox.setCurrentIndex(0)
        
        # 定义 jianer_setup_lgr 中的可选日志等级
        self.jianer_setup_lgr.SplitPushButton.clear()
        self.jianer_setup_lgr.SplitPushButton.addItem("DEBUG")
        self.jianer_setup_lgr.SplitPushButton.addItem("TRACE")
        self.jianer_setup_lgr.SplitPushButton.addItem("INFO")
        self.jianer_setup_lgr.SplitPushButton.addItem("WARNING")
        self.jianer_setup_lgr.SplitPushButton.addItem("ERROR")
        self.jianer_setup_lgr.SplitPushButton.addItem("CRITICAL")
        self.jianer_setup_lgr.SplitPushButton.setCurrentIndex(0)

        # 添加子界面
        self.addSubInterface(self.jianer_setup_wizard, QIcon(os.path.abspath('.//wizardWindows/icon.png')), "欢迎")
        self.addSubInterface(self.jianer_setup_basic, FluentIcon.COPY, "基本信息设置")
        self.addSubInterface(self.jianer_setup_ai, FluentIcon.TRANSPARENT, "AI 设置")
        self.addSubInterface(self.jianer_setup_pre, FluentIcon.PENCIL_INK, "AI 预设")
        self.addSubInterface(self.jianer_setup_TTS, FluentIcon.MIX_VOLUMES, "AI 语音回复")
        self.addSubInterface(self.jianer_setup_others, FluentIcon.CAFE, "其他设置")
        self.addSubInterface(self.jianer_setup_lgr, FluentIcon.DEVELOPER_TOOLS, "高级设置")
        self.addSubInterface(self.jianer_setup_advanced, FluentIcon.APPLICATION, "框架设置")
        self.addSubInterface(self.jianer_setup_plugins, FluentIcon.CODE, "插件中心")
        self.addSubInterface(self.jianer_setup_workflow, FluentIcon.ROBOT, "工作流管理")
        self.addSubInterface(self.jianer_setup_apply, FluentIcon.SAVE_AS, "核对并应用设置")
        self.addSubInterface(self.jianer_setup_about, FluentIcon.INFO, "关于", NavigationItemPosition.BOTTOM)
        self.stackedWidget.currentChanged.connect(self.update_plain_text)

        # 应用设置
        self.jianer_setup_apply.PrimaryPushButton.clicked.connect(self.save_settings)
        self.jianer_setup_apply.PrimaryPushButton_2.clicked.connect(self.start_bot_with_ui)
        
        self.read_settings()
        self.splashScreen.finish()
        
        # 初始化机器人进程管理器
        self.bot_process = BotProcessManager(self)
        self.bot_process.outputReceived.connect(self.append_log_output)
        self.bot_process.errorReceived.connect(self.append_log_error)
        self.bot_process.processFinished.connect(self.on_bot_process_finished)
        
        # 初始化日志显示
        self.init_console_log()
        
        # 初始化工作流管理器
        self.init_workflow_manager()

    def showEvent(self, event):
        super().showEvent(event)

    @Slot(object)
    def receive_intelliMarkets(self, instance): 
        print('checking_intelliMarkets')
        self.intelliMarkets = instance
        print('checked')
        if self.intelliMarkets.repo is None:
            self.jianer_setup_plugins.ComboBox.setEnabled(True)
            self.jianer_setup_plugins.LoadingBar.setVisible(False)
            self.jianer_setup_plugins.SearchButton.setEnabled(True)
            InfoBar.warning(title='插件中心连接失败', content="请检查 Github 连接状态，使用代理可能解决此问题。\n请重新选择筛选条件以刷新插件中心。", orient=Qt.Horizontal,
                isClosable=True,   # enable close button
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self
            )
        else:
            self.update_plain_plugins()

    # def start_task(self, function, callback):
    #     task = TaskRunner(function)
    #     task.finished_signal.connect(callback)
    #     self.threadpool.start(task)

    async def load_pre_voices(self):
        global voices
        try:
            voices = await edge_tts.voices.list_voices()
        except:
            InfoBar.error(title='Microsoft 服务器连接失败', content="请检查网络连接状态，然后重新启动设置向导。", orient=Qt.Horizontal,
                isClosable=True,   # enable close button
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self
            )
        # print(voices)

    # def Initialization_Intellimarket(self):
    #     worker = TaskRunner(IntelliMarkets.gen_token)
    #     worker.set_name(name="gen_token")

    #     @Slot(object) 
    #     def handle_token_result(result):
    #         try:
    #             if isinstance(result, (tuple, list)) and len(result) == 2:
    #                 new_instance = IntelliMarkets(*result)
    #             else:
    #                 new_instance = IntelliMarkets(result)
                    
    #             # 线程安全地更新实例
    #             QMetaObject.invokeMethod(self, "update_intelli_markets", 
    #                                 Qt.ConnectionType.QueuedConnection,
    #                                 Q_ARG(object, new_instance))
    #         except Exception as e:
    #             print(f"Token生成失败: {e}")

    #     @Slot(object)
    #     def update_intelli_markets(self, new_instance):
    #         """线程安全地更新intelliMarkets实例"""
    #         self.intelliMarkets = new_instance
    #         print("Token生成完成，实例已更新")

    #     worker.signals.finished.connect(handle_token_result)

    #     # 自动清理设置
    #     worker.setAutoDelete(True)  # 替代注释掉的错误代码

    #     print("Generating token...")
    #     QThreadPool.globalInstance().start(worker)
        
    def new_preset(self, preset_file, preset_title, preset_intro, preset_uins, with_save=False):
        # self.jianer_setup_pre.gridLayout.addWidget(self.template_preset)
        global preset_layout


        # 唯一标识符看起来太乱了，这里使用随机数生成预设id
        preset_id: str = ""
        if preset_file == None:
            while True:
                preset_id = "p" + str(random.randint(1000000, 9999999))
                if not os.path.exists(os.path.join(presets_tool.PRESET_DIR, f"{preset_id}.txt")):
                    with open(os.path.join(presets_tool.PRESET_DIR, f"{preset_id}.txt"), 'w') as f:
                        f.write("")
                        f.close()

                    break
        else:
            preset_id = preset_file

        preset_layout_name: str = f"Label_Icon_{preset_id}"
        preset_path = os.path.join(presets_tool.PRESET_DIR, f"{preset_id}.txt")
        self.jianer_setup_pre.Label_Icon_2 = CardWidget(self.jianer_setup_pre.scrollAreaWidgetContents)
        self.jianer_setup_pre.Label_Icon_2.setMinimumSize(QtCore.QSize(0, 138))
        self.jianer_setup_pre.Label_Icon_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.jianer_setup_pre.Label_Icon_2.setObjectName(preset_layout_name)
        self.jianer_setup_pre.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.jianer_setup_pre.Label_Icon_2)
        self.jianer_setup_pre.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.jianer_setup_pre.horizontalLayout_9.addItem(spacerItem2)
        self.jianer_setup_pre.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.jianer_setup_pre.verticalLayout_9.setObjectName("verticalLayout_9")
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.jianer_setup_pre.verticalLayout_9.addItem(spacerItem3)
        self.jianer_setup_pre.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.jianer_setup_pre.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.jianer_setup_pre.SubtitleLabel = SubtitleLabel(self.jianer_setup_pre.Label_Icon_2)
        font = QtGui.QFont()
        font.setFamily("HarmonyOS Sans SC")
        font.setPointSize(15)
        font.setBold(False)
        self.jianer_setup_pre.SubtitleLabel.setFont(font)
        self.jianer_setup_pre.SubtitleLabel.setObjectName("SubtitleLabel")
        self.jianer_setup_pre.horizontalLayout_3.addWidget(self.jianer_setup_pre.SubtitleLabel)
        self.jianer_setup_pre.PreTitle = LineEdit(self.jianer_setup_pre.Label_Icon_2)
        self.jianer_setup_pre.PreTitle.setMaximumSize(QtCore.QSize(16777215, 38))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(13)
        font.setBold(False)
        self.jianer_setup_pre.PreTitle.setFont(font)
        self.jianer_setup_pre.PreTitle.setObjectName(f"{preset_layout_name}-Title")
        self.jianer_setup_pre.horizontalLayout_3.addWidget(self.jianer_setup_pre.PreTitle)
        self.jianer_setup_pre.verticalLayout_9.addLayout(self.jianer_setup_pre.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.jianer_setup_pre.verticalLayout_9.addItem(spacerItem4)
        self.jianer_setup_pre.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.jianer_setup_pre.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.jianer_setup_pre.SubtitleLabel_2 = SubtitleLabel(self.jianer_setup_pre.Label_Icon_2)
        font = QtGui.QFont()
        font.setFamily("HarmonyOS Sans SC")
        font.setPointSize(14)
        font.setBold(False)
        self.jianer_setup_pre.SubtitleLabel_2.setFont(font)
        self.jianer_setup_pre.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.jianer_setup_pre.horizontalLayout_4.addWidget(self.jianer_setup_pre.SubtitleLabel_2)
        self.jianer_setup_pre.PreTitle_2 = LineEdit(self.jianer_setup_pre.Label_Icon_2)
        self.jianer_setup_pre.PreTitle_2.setMaximumSize(QtCore.QSize(16777215, 33))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        font.setBold(False)
        self.jianer_setup_pre.PreTitle_2.setFont(font)
        self.jianer_setup_pre.PreTitle_2.setObjectName(f"{preset_layout_name}-Intro")
        self.jianer_setup_pre.horizontalLayout_4.addWidget(self.jianer_setup_pre.PreTitle_2)
        self.jianer_setup_pre.verticalLayout_9.addLayout(self.jianer_setup_pre.horizontalLayout_4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.jianer_setup_pre.verticalLayout_9.addItem(spacerItem5)
        self.jianer_setup_pre.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.jianer_setup_pre.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.jianer_setup_pre.SubtitleLabel_3 = SubtitleLabel(self.jianer_setup_pre.Label_Icon_2)
        font = QtGui.QFont()
        font.setFamily("HarmonyOS Sans SC")
        font.setPointSize(13)
        font.setBold(False)
        self.jianer_setup_pre.SubtitleLabel_3.setFont(font)
        self.jianer_setup_pre.SubtitleLabel_3.setObjectName("SubtitleLabel_3")
        self.jianer_setup_pre.horizontalLayout_5.addWidget(self.jianer_setup_pre.SubtitleLabel_3)
        self.jianer_setup_pre.PreTitle_3 = PresetLineEdit(self.jianer_setup_pre.Label_Icon_2)
        self.jianer_setup_pre.PreTitle_3.setMaximumSize(QtCore.QSize(16777215, 33))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        font.setBold(False)
        self.jianer_setup_pre.PreTitle_3.setFont(font)
        self.jianer_setup_pre.PreTitle_3.setObjectName(f"{preset_layout_name}-Uins")
        self.jianer_setup_pre.horizontalLayout_5.addWidget(self.jianer_setup_pre.PreTitle_3)
        self.jianer_setup_pre.verticalLayout_9.addLayout(self.jianer_setup_pre.horizontalLayout_5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.jianer_setup_pre.verticalLayout_9.addItem(spacerItem6)
        self.jianer_setup_pre.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.jianer_setup_pre.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem7 = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.jianer_setup_pre.horizontalLayout_6.addItem(spacerItem7)
        
        if not preset_id == "Normal": 
            self.jianer_setup_pre.PushButton = PushButton(self.jianer_setup_pre.Label_Icon_2)
            self.jianer_setup_pre.PushButton.setObjectName("PushButton")
            self.jianer_setup_pre.PushButton.clicked.connect(lambda: self.del_preset(preset_layout_name))
            self.jianer_setup_pre.horizontalLayout_6.addWidget(self.jianer_setup_pre.PushButton)
            
        self.jianer_setup_pre.PrimaryPushButton = PrimaryPushButton(self.jianer_setup_pre.Label_Icon_2)
        self.jianer_setup_pre.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.jianer_setup_pre.PrimaryPushButton.clicked.connect(lambda: os.startfile(preset_path))
        self.jianer_setup_pre.horizontalLayout_6.addWidget(self.jianer_setup_pre.PrimaryPushButton)
        spacerItem8 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.jianer_setup_pre.horizontalLayout_6.addItem(spacerItem8)
        self.jianer_setup_pre.verticalLayout_9.addLayout(self.jianer_setup_pre.horizontalLayout_6)
        spacerItem9 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.jianer_setup_pre.verticalLayout_9.addItem(spacerItem9)
        self.jianer_setup_pre.horizontalLayout_9.addLayout(self.jianer_setup_pre.verticalLayout_9)
        spacerItem10 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.jianer_setup_pre.horizontalLayout_9.addItem(spacerItem10)
        self.jianer_setup_pre.gridLayout.addWidget(self.jianer_setup_pre.Label_Icon_2, len(preset_layout) + 6, 0, 1, 1)

        preset_layout.append(preset_layout_name)
        print(preset_layout)

        _translate = QtCore.QCoreApplication.translate
        self.jianer_setup_pre.SubtitleLabel.setText(_translate("Form", "预设名称："))
        self.jianer_setup_pre.PreTitle.setText(_translate("Form", preset_title))
        self.jianer_setup_pre.SubtitleLabel_2.setText(_translate("Form", "预设介绍："))
        self.jianer_setup_pre.PreTitle_2.setText(_translate("Form", preset_intro))
        self.jianer_setup_pre.SubtitleLabel_3.setText(_translate("Form", "用户QQ号："))
        self.jianer_setup_pre.PreTitle_3.setText(_translate("Form", preset_uins))
        if not preset_id == "Normal": self.jianer_setup_pre.PushButton.setText(_translate("Form", "删除"))
        self.jianer_setup_pre.PrimaryPushButton.setText(_translate("Form", "编辑预设内容" if not preset_id == "Normal" else "编辑默认预设内容"))

        if with_save:
            GenerateSettings._prerequisites(self)
            GenerateSettings.save_presets(self)

    def del_preset(self, preset_layout_name: str):
        global preset_layout
        print(preset_layout_name)
        w = MessageBox("确认删除？", "在你最终做好决策之前，请不要点击确认按钮，否则预设将会被立即删除。", self)
        if not w.exec():
            return
            
        row_to_delete = -1
        print("删除预设")
        for i in range(self.jianer_setup_pre.gridLayout.count()):
            item = self.jianer_setup_pre.gridLayout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if widget.objectName() == preset_layout_name:
                    row_to_delete = self.jianer_setup_pre.gridLayout.getItemPosition(i)[0]
                    self.jianer_setup_pre.gridLayout.removeItem(item)
                    widget.setParent(None)
                    break # 找到并删除后，退出循环

        preset_layout.remove(preset_layout_name)
        os.remove(os.path.join(presets_tool.PRESET_DIR, f"{preset_layout_name.split(r'_')[-1]}.txt"))
        print(preset_layout)
        
        items_to_move = []
        for i in range(self.jianer_setup_pre.gridLayout.count()):
            item = self.jianer_setup_pre.gridLayout.itemAt(i)
            if item and item.widget():
                row, col, rowspan, colspan = self.jianer_setup_pre.gridLayout.getItemPosition(i)
                if row > row_to_delete:  # 下方的控件
                    items_to_move.append((item.widget(), row, col, rowspan, colspan))

        # 4. 移动控件
        for widget, row, col, rowspan, colspan in items_to_move:
            self.jianer_setup_pre.gridLayout.removeWidget(widget)  # 先从布局中移除
            self.jianer_setup_pre.gridLayout.addWidget(widget, row - 1, col, rowspan, colspan)  # 添加到新的位置

        GenerateSettings._prerequisites(self)
        GenerateSettings.save_presets(self)
        
    def update_plain_text(self):
        global voices, config_content, appSettings_content, presets_content, presets_page_tip_showed
        if self.stackedWidget.currentWidget() == self.jianer_setup_apply:
            self.jianer_setup_apply.LargeTitleLabel.setText("核对设置清单并生成设置")
            self.jianer_setup_apply.LargeTitleLabel.setTextColor()            
            self.gen_all_settings()

            config_text = f'''——————QQ机器人 配置设置——————
    {config_content}'''
            
            presets_text = f'''——————AI预设 配置设置——————
    {presets_content}'''
            
            app_settings_text = f'''——————框架设置——————
    {appSettings_content}'''

            self.jianer_setup_apply.PlainTextEdit.setPlainText('\n\n'.join([config_text, presets_text, app_settings_text]))

        elif self.stackedWidget.currentWidget() == self.jianer_setup_about:
            self.jianer_setup_about.SubtitleLabel_7.setText(f"请在QQ群中发送消息 {self.jianer_setup_basic.LineEdit_5.text()}关于 来查看更详细的关于信息。")

        elif self.stackedWidget.currentWidget() == self.jianer_setup_pre:
            if not presets_page_tip_showed:
                presets_page_tip_showed = True
                InfoBar.info(
                    title='请注意保存',
                    content="在编辑完任何预设配置或预设内容后，\n请转到 “核对并应用设置” 页面并点击 【应用】以使配置生效。",
                    orient=Qt.Horizontal,
                    isClosable=True,   # enable close button
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=6000,
                    parent=self
                )
                
    def update_plain_plugins(self):
        global local_plugins_list, updatable_plugin_list

        self.jianer_setup_plugins.ComboBox.setEnabled(False)
        self.jianer_setup_plugins.LoadingBar.setVisible(True)
        self.jianer_setup_plugins.SearchButton.setEnabled(False) # 初始化显示
        IntelliMarkets.del_all_plugin_UI(self.jianer_setup_plugins)
        local_plugins_list = PluginsManager.get_all_plugin_names()
        if self.jianer_setup_plugins.ComboBox.currentIndex() == 0:
            
            if self.intelliMarkets is None or self.intelliMarkets.repo is None:
                self.jianer_setup_plugins.SubtitleLabel_5.setText("    请等待，正在连接至插件中心……")
                print("请等待，正在连接至插件中心……")
                QApplication.processEvents()
                self.init_intelliMarkets()
                return
            
            worker = TaskRunner(self.intelliMarkets.get_all_plugins)
            worker.set_name(name="get_all_plugins")
            worker.signals.finished.connect(lambda result: self.get_all_intro(result))
            # worker.signals.finished.connect(worker.autoDelete)  # 自动清理

            print("loading…………")
            QThreadPool.globalInstance().start(worker)
                
        elif self.jianer_setup_plugins.ComboBox.currentIndex() == 1:
            for name in local_plugins_list:
                if name in plugins_list and plugins_list[name]:
                    IntelliMarkets.new_plugin(self.jianer_setup_plugins, name, plugins_list[name]['intro'], False)
                else:
                    IntelliMarkets.new_plugin(self.jianer_setup_plugins, name, is_all=False)

            self.jianer_setup_plugins.LoadingBar.setVisible(False)
            self.jianer_setup_plugins.ComboBox.setEnabled(True)
            self.jianer_setup_plugins.SearchButton.setEnabled(True)
        elif self.jianer_setup_plugins.ComboBox.currentIndex() == 2: 
            thread_pool = QThreadPool.globalInstance()

            print(f"对 {local_plugins_list} 进行检查更新")
            for name in local_plugins_list:

                def update_or_not(r, n=name):
                    if r:
                        print(f"{n} 需要更新")
                        updatable_plugin_list.append(n)
                        if n in plugins_list and plugins_list[n]:
                            IntelliMarkets.new_plugin(self.jianer_setup_plugins, n, plugins_list[n]['intro'], False, True)
                        else:
                            IntelliMarkets.new_plugin(self.jianer_setup_plugins, n, is_all=False, is_to_update=True)
                    else:
                        print(f"{n} 无需更新")

                    self.jianer_setup_plugins.LoadingBar.setVisible(False)
                    self.jianer_setup_plugins.ComboBox.setEnabled(True)
                    self.jianer_setup_plugins.SearchButton.setEnabled(True)

                try:    
                    worker = TaskRunner(self.intelliMarkets.check_for_update, name)
                    worker.set_name(name=f"{name}-checking")
                    worker.signals.finished.connect(lambda result, nm=name: update_or_not(result, nm))

                    updatable_plugin_list.clear()
                    thread_pool.start(worker)
                except Exception as e:
                    print(f"TaskRunner 发生异常: {e}") 

        self.jianer_setup_plugins.SubtitleLabel_5.setText(QCoreApplication.translate("Form", u"    \u5728\u6b64\u5904\uff0c\u53d1\u6325\u7b80\u513f\u7684\u65e0\u9650\u53ef\u80fd", None))
        # QApplication.processEvents() # 高危！！！

    def search_plain_plugins(self, text: str):
        global local_plugins_list, plugins_list, updatable_plugin_list

        self.jianer_setup_plugins.ComboBox.setEnabled(False)
        self.jianer_setup_plugins.SearchButton.setEnabled(False)
        self.jianer_setup_plugins.LoadingBar.setVisible(True) # 初始化显示
        IntelliMarkets.del_all_plugin_UI(self.jianer_setup_plugins)
        local_plugins_list = PluginsManager.get_all_plugin_names()
        if self.jianer_setup_plugins.ComboBox.currentIndex() == 0:
            for key in plugins_list:
                intro = plugins_list[key]['intro']
                if text in str(key) or text in str(intro):
                    if not key in local_plugins_list:
                        IntelliMarkets.new_plugin(self.jianer_setup_plugins, key, intro)
                    else:
                        IntelliMarkets.new_plugin(self.jianer_setup_plugins, key, intro, False)
                
            self.jianer_setup_plugins.LoadingBar.setVisible(False)
            self.jianer_setup_plugins.ComboBox.setEnabled(True)
            self.jianer_setup_plugins.SearchButton.setEnabled(True)
        elif self.jianer_setup_plugins.ComboBox.currentIndex() == 1:
            for name in local_plugins_list:
                if name in plugins_list and plugins_list[name]:
                    if text in name or text in plugins_list[name]['intro']:
                        IntelliMarkets.new_plugin(self.jianer_setup_plugins, name, plugins_list[name]['intro'], False)
                else:
                    if text in name:
                        IntelliMarkets.new_plugin(self.jianer_setup_plugins, name, is_all=False)

            self.jianer_setup_plugins.LoadingBar.setVisible(False)
            self.jianer_setup_plugins.ComboBox.setEnabled(True)
            self.jianer_setup_plugins.SearchButton.setEnabled(True)
        elif self.jianer_setup_plugins.ComboBox.currentIndex() == 2: 
            for name in updatable_plugin_list:
                if name in plugins_list and plugins_list[name]:
                    if text in name or text in plugins_list[name]['intro']:
                        IntelliMarkets.new_plugin(self.jianer_setup_plugins, name, plugins_list[name]['intro'], False, True)
                else:
                    if text in name:
                        IntelliMarkets.new_plugin(self.jianer_setup_plugins, name, is_all=False, is_to_update=True)

            self.jianer_setup_plugins.LoadingBar.setVisible(False)
            self.jianer_setup_plugins.ComboBox.setEnabled(True)
            self.jianer_setup_plugins.SearchButton.setEnabled(True)

        self.jianer_setup_plugins.SubtitleLabel_5.setText(QCoreApplication.translate("Form", u"    \u5728\u6b64\u5904\uff0c\u53d1\u6325\u7b80\u513f\u7684\u65e0\u9650\u53ef\u80fd", None))
        

    def init_intelliMarkets(self):
        print("init_intelliMarkets")
        self.jianer_setup_plugins.ComboBox.setEnabled(False)
        self.jianer_setup_plugins.SearchButton.setEnabled(False)

        def init_intelliMarkets(): return IntelliMarkets()
        worker = TaskRunner(init_intelliMarkets)
        worker.set_name(name="gen_token")
        worker.signals.finished.connect(lambda r: self.receive_intelliMarkets(r))
        # worker.signals.finished.connect(worker.autoDelete)  # 自动清理
        QThreadPool.globalInstance().start(worker)

    def gen_all_settings(self):
        GenerateSettings.gen_config(GenerateSettings, 
            self.jianer_setup_basic.LineEdit_2.text(), 
            self.jianer_setup_lgr.LineEdit.text(), 
            self.jianer_setup_lgr.LineEdit_6.text(), 
            self.jianer_setup_ai.LineEdit_6.text(), 
            self.jianer_setup_ai.LineEdit.text(), 
            self.jianer_setup_basic.LineEdit.text(), 
            self.jianer_setup_basic.LineEdit_6.text(),   
            self.jianer_setup_basic.LineEdit_2.text(), 
            self.jianer_setup_basic.PlainTextEdit.toPlainText(), 
            self.jianer_setup_basic.LineEdit_5.text(), 
            self.jianer_setup_lgr.SplitPushButton.currentText(), 
            self.jianer_setup_lgr.PlainTextEdit.toPlainText(), 
            self.jianer_setup_ai.DeepSeekeyEdit.text(), 
            self.jianer_setup_others.SloganText.text(), 
            self.jianer_setup_others.NiceWords.toPlainText(), 
            self.jianer_setup_TTS.voiceColor.text(), 
            self.jianer_setup_TTS.ttsRate.text(), 
            self.jianer_setup_TTS.ttsVolume.text(), 
            self.jianer_setup_TTS.ttsPitCh.text(), 
            self.jianer_setup_others.PokeWords.toPlainText(),
            self.jianer_setup_ai.ComboBox.currentText()) # -> config_content
        
        GenerateSettings.gen_appSettings(GenerateSettings, 
            self.jianer_setup_basic.LineEdit_4.text(), 
            self.jianer_setup_lgr.LineEdit.text(), 
            self.jianer_setup_lgr.LineEdit_6.text(), 
            self.jianer_setup_advanced.SplitPushButton.currentText()) # -> appSettings_content
        
        GenerateSettings._prerequisites(self) # -> presets_content

            
    def read_settings(self):
        global presets_tool

        for data in presets.values():
            uins = list(data['uid']) if not isinstance(data['uid'], list) else data['uid']
            uin_string = ", ".join(map(str, uins))
            file_name, _ = os.path.splitext(os.path.basename(data['path']))
            self.new_preset(file_name, data['name'], data['info'], uin_string)
            
        have_normal_tts = False
        self.jianer_setup_TTS.voiceColor.clear()

        if voices is not None:
            for voice in voices:
                self.jianer_setup_TTS.voiceColor.addItem(voice["ShortName"])
                if "zh-CN-XiaoyiNeural" == str(voice["ShortName"]):
                    have_normal_tts = True
            
        self.init_intelliMarkets()
        print("load completed.")
            
        # 加载QQ机器人设置
        if os.path.isfile(".\\config.json"):
            with open(".\\config.json", "r", encoding="utf-8") as f:
                settings = f.read()
                f.close()
                
                data = json.loads(settings)
                connection = data["Connection"]
                others = data["Others"]

                self.jianer_setup_basic.LineEdit_2.setText("\n".join(str(item) for item in data["owner"]))
                self.jianer_setup_lgr.LineEdit.setText(str(connection["host"]))
                self.jianer_setup_lgr.LineEdit_6.setText(str(connection["port"]))
                self.jianer_setup_ai.LineEdit_6.setText(str(others["gemini_key"]))
                self.jianer_setup_ai.LineEdit.setText(str(others["openai_key"]))
                self.jianer_setup_ai.DeepSeekeyEdit.setText(str(others["deepseek_key"]))
                self.jianer_setup_basic.LineEdit.setText(str(others["bot_name"]))
                self.jianer_setup_basic.LineEdit_6.setText(str(others["bot_name_en"]))
                self.jianer_setup_basic.LineEdit_2.setText("\n".join(str(item) for item in others["ROOT_User"]))
                self.jianer_setup_basic.PlainTextEdit.setPlainText("\n".join(str(item) for item in others["Auto_approval"]))
                self.jianer_setup_basic.LineEdit_5.setText(str(others["reminder"]))
                self.jianer_setup_lgr.SplitPushButton.setCurrentText(str(data["Log_level"]))
                self.jianer_setup_lgr.PlainTextEdit.setPlainText("\n".join(str(item) for item in data["black_list"]))
                self.jianer_setup_TTS.ttsRate.setCurrentText(str(others["TTS"]["rate"]))
                self.jianer_setup_TTS.ttsVolume.setCurrentText(str(others["TTS"]["volume"]))
                self.jianer_setup_TTS.ttsPitCh.setCurrentText(str(others["TTS"]["pitch"]))
                self.jianer_setup_TTS.voiceColor.setCurrentText(str(others["TTS"]["voiceColor"]))
                self.jianer_setup_others.SloganText.setText(str(others["slogan"]))
                self.jianer_setup_others.NiceWords.setPlainText("\n".join(str(item) for item in others["compliment"]))
                self.jianer_setup_others.PokeWords.setPlainText("\n".join(str(item) for item in others["poke_rejection_phrases"]))
                
                match others["default_mode"]:
                    case "Ds":
                        self.jianer_setup_ai.ComboBox.setCurrentIndex(0)
                    case "Pixmap":
                        self.jianer_setup_ai.ComboBox.setCurrentIndex(1)
                    case "Net":
                        self.jianer_setup_ai.ComboBox.setCurrentIndex(2)
                    case "Normal":
                        self.jianer_setup_ai.ComboBox.setCurrentIndex(3)
                    case _:
                        pass

        else:
            self.jianer_setup_TTS.ttsRate.setCurrentIndex(10)
            self.jianer_setup_TTS.ttsVolume.setCurrentIndex(10)
            self.jianer_setup_TTS.ttsPitCh.setCurrentIndex(10)
            if have_normal_tts: self.jianer_setup_TTS.voiceColor.setCurrentText("zh-CN-XiaoyiNeural")
                
        # 加载框架设置
        if os.path.isfile(".\\appsettings.json"):
            with open(".\\appsettings.json", "r", encoding="utf-8") as f:
                settings = f.read()
                f.close()
                
                data = json.loads(settings)
                Account = data["Account"]
                print(Account)
                Implementations = data["Implementations"][0]
                
                self.jianer_setup_basic.LineEdit_4.setText(str(Account["Uin"]))
                self.jianer_setup_lgr.LineEdit.setText(str(Implementations["Host"]))
                self.jianer_setup_lgr.LineEdit_6.setText(str(Implementations["Port"]))
                
                print(str(data["SignServerUrl"]))
                match str(data["SignServerUrl"]):
                    case "https://sign.lagrangecore.org/api/sign/30366":
                        self.jianer_setup_advanced.SplitPushButton.setCurrentIndex(0)
                    case "http://106.54.14.24:8084/api/sign/30366":
                        self.jianer_setup_advanced.SplitPushButton.setCurrentIndex(1)
                    case "https://sign.0w0.ing/api/sign/30366":
                        self.jianer_setup_advanced.SplitPushButton.setCurrentIndex(2)
                    case _:
                        pass
            
    def save_settings(self):
        global config_content, appSettings_content
        
        self.gen_all_settings()
        
        if config_content is None or appSettings_content is None:
            self.jianer_setup_apply.LargeTitleLabel.setText("设置的配置有误，请核对设置清单")
            self.jianer_setup_apply.LargeTitleLabel.setTextColor(QColor(255, 60, 48), QColor(255, 60, 48))
        else:
            try:
                with open(".\\config.json", "w", encoding="utf-8") as f:
                    f.write(config_content)
                    f.close()
                
                with open(".\\appsettings.json", "w", encoding="utf-8") as f:
                    f.write(appSettings_content)
                    f.close()
                    
                GenerateSettings.save_presets(self)
                
                self.jianer_setup_apply.LargeTitleLabel.setText("已成功保存")
                self.jianer_setup_apply.LargeTitleLabel.setTextColor(QColor(82, 210, 97), QColor(82, 210, 97))
            except Exception as e:
                traceback.print_exc()
                self.jianer_setup_apply.LargeTitleLabel.setText("无法写入文件，请检查权限")
                self.jianer_setup_apply.LargeTitleLabel.setTextColor(QColor(255, 60, 48), QColor(255, 60, 48))
    
    def init_workflow_manager(self):
        """初始化工作流管理器"""
        try:
            print("开始初始化工作流管理器...")
            from Tools.workflow_manager import WorkflowManager
            print("工作流管理器模块导入成功")
            
            self.workflow_manager = WorkflowManager()
            print("工作流管理器实例创建成功")
            
            self.jianer_setup_workflow.set_workflow_manager(self.workflow_manager)
            print("工作流管理器设置完成")
            
        except Exception as e:
            print(f"初始化工作流管理器失败: {e}")
            import traceback
            traceback.print_exc()
            # 设置一个空的工作流管理器，防止程序崩溃
            self.workflow_manager = None
            print("工作流管理器初始化失败，但程序将继续运行")
    
    def add_workflow_button(self):
        """手动添加工作流按钮到向导界面"""
        try:
            from qfluentwidgets import ElevatedCardWidget, IconWidget, TitleLabel, SubtitleLabel
            from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
            from PySide6.QtCore import QSize
            from PySide6.QtGui import QFont
            
            # 创建工作流按钮
            self.jianer_setup_wizard.WorkflowIconButton = ElevatedCardWidget(self.jianer_setup_wizard.scrollAreaWidgetContents)
            self.jianer_setup_wizard.WorkflowIconButton.setObjectName("WorkflowIconButton")
            self.jianer_setup_wizard.WorkflowIconButton.setMaximumSize(QSize(16777215, 100))
            
            # 水平布局
            horizontal_layout = QHBoxLayout(self.jianer_setup_wizard.WorkflowIconButton)
            horizontal_layout.setObjectName("WorkflowHorizontalLayout")
            
            # 左侧间距
            left_spacer = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
            horizontal_layout.addItem(left_spacer)
            
            # 图标
            icon_widget = IconWidget(self.jianer_setup_wizard.WorkflowIconButton)
            icon_widget.setObjectName("WorkflowIconWidget")
            icon_widget.setEnabled(True)
            icon_widget.setMinimumSize(QSize(40, 40))
            icon_widget.setMaximumSize(QSize(40, 40))
            icon_widget.setIcon(FluentIcon.ROBOT)
            horizontal_layout.addWidget(icon_widget)
            
            # 中间间距
            middle_spacer = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
            horizontal_layout.addItem(middle_spacer)
            
            # 垂直布局用于文字
            vertical_layout = QVBoxLayout()
            vertical_layout.setObjectName("WorkflowVerticalLayout")
            
            # 上方间距
            top_spacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
            vertical_layout.addItem(top_spacer)
            
            # 标题
            title_label = TitleLabel(self.jianer_setup_wizard.WorkflowIconButton)
            title_label.setObjectName("WorkflowTitleLabel")
            title_label.setMaximumSize(QSize(16777215, 50))
            font = QFont()
            font.setFamilies(["HarmonyOS Sans SC"])
            font.setPointSize(21)
            font.setBold(False)
            title_label.setFont(font)
            title_label.setText("工作流管理")
            vertical_layout.addWidget(title_label)
            
            # 副标题
            subtitle_label = SubtitleLabel(self.jianer_setup_wizard.WorkflowIconButton)
            subtitle_label.setObjectName("WorkflowSubtitleLabel")
            font2 = QFont()
            font2.setFamilies(["HarmonyOS Sans SC"])
            font2.setPointSize(12)
            font2.setBold(False)
            subtitle_label.setFont(font2)
            subtitle_label.setText("配置和管理自动化工作流，让机器人更智能地响应用户。")
            subtitle_label.setWordWrap(True)
            vertical_layout.addWidget(subtitle_label)
            
            # 下方间距
            bottom_spacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
            vertical_layout.addItem(bottom_spacer)
            
            horizontal_layout.addLayout(vertical_layout)
            
            # 添加到网格布局（在插件中心之后）
            grid_layout = self.jianer_setup_wizard.gridLayout
            row_count = grid_layout.rowCount()
            grid_layout.addWidget(self.jianer_setup_wizard.WorkflowIconButton, row_count, 0, 1, 1)
            
            # 连接点击事件
            self.jianer_setup_wizard.WorkflowIconButton.clicked.connect(lambda: self.switchTo(self.jianer_setup_workflow))
            
            print("工作流按钮添加成功")
            
        except Exception as e:
            print(f"添加工作流按钮失败: {e}")
    
    def init_console_log(self):
        """初始化控制台日志显示"""
        try:
            # 检查是否已经有日志显示区域
            if hasattr(self.jianer_setup_apply, 'console_log'):
                return
            
            # 创建日志显示组件
            self.jianer_setup_apply.console_log = QTextEdit()
            self.jianer_setup_apply.console_log.setReadOnly(True)
            self.jianer_setup_apply.console_log.setStyleSheet("""
                QTextEdit {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 10pt;
                    border: 1px solid #555;
                }
            """)
            self.jianer_setup_apply.console_log.setMaximumHeight(200)
            self.jianer_setup_apply.console_log.setMinimumHeight(150)
            
            # 创建一个分割器来分割原有内容和日志
            if hasattr(self.jianer_setup_apply, 'splitter'):
                return
                
            self.jianer_setup_apply.splitter = QSplitter(Qt.Orientation.Vertical)
            
            # 获取原有的主布局
            main_layout = self.jianer_setup_apply.layout()
            if main_layout is None:
                # 如果没有布局，创建一个
                main_layout = QVBoxLayout(self.jianer_setup_apply)
                self.jianer_setup_apply.setLayout(main_layout)
            
            # 创建上部内容的容器
            top_widget = QWidget()
            top_layout = QVBoxLayout(top_widget)
            
            # 将原有的所有子组件移动到上部容器
            while main_layout.count() > 0:
                item = main_layout.takeAt(0)
                if item.widget():
                    top_layout.addWidget(item.widget())
                elif item.layout():
                    top_layout.addLayout(item.layout())
            
            # 将上部容器和日志组件添加到分割器
            self.jianer_setup_apply.splitter.addWidget(top_widget)
            self.jianer_setup_apply.splitter.addWidget(self.jianer_setup_apply.console_log)
            
            # 设置分割比例
            self.jianer_setup_apply.splitter.setStretchFactor(0, 3)  # 上部占更多空间
            self.jianer_setup_apply.splitter.setStretchFactor(1, 1)  # 日志区域
            
            # 将分割器添加到主布局
            main_layout.addWidget(self.jianer_setup_apply.splitter)
            
            # 添加初始日志
            self.append_log_output(f"[小依配置助手] 日志系统初始化完成 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
        except Exception as e:
            print(f"初始化控制台日志失败: {e}")
    
    def append_log_output(self, text):
        """添加正常输出日志"""
        if hasattr(self.jianer_setup_apply, 'console_log'):
            # 处理多行输出
            lines = text.splitlines()
            for line in lines:
                if line.strip():  # 只处理非空行
                    # 添加时间戳和颜色
                    timestamp = datetime.datetime.now().strftime('[%H:%M:%S]')
                    formatted_text = f"<span style='color: #00ff00;'>{timestamp}</span> <span style='color: #ffffff;'>{line.replace('<', '&lt;').replace('>', '&gt;')}</span>"
                    
                    self.jianer_setup_apply.console_log.append(formatted_text)
            
            # 如果有空行，也要显示
            if text.endswith('\n') or text.endswith('\r\n'):
                self.jianer_setup_apply.console_log.append("")
                
            # 自动滚动到底部
            cursor = self.jianer_setup_apply.console_log.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.jianer_setup_apply.console_log.setTextCursor(cursor)
    
    def append_log_error(self, text):
        """添加错误输出日志"""
        if hasattr(self.jianer_setup_apply, 'console_log'):
            # 处理多行输出
            lines = text.splitlines()
            for line in lines:
                if line.strip():  # 只处理非空行
                    # 添加时间戳和红色
                    timestamp = datetime.datetime.now().strftime('[%H:%M:%S]')
                    formatted_text = f"<span style='color: #ff4444;'>{timestamp} [ERROR]</span> <span style='color: #ffaaaa;'>{line.replace('<', '&lt;').replace('>', '&gt;')}</span>"
                    
                    self.jianer_setup_apply.console_log.append(formatted_text)
            
            # 如果有空行，也要显示
            if text.endswith('\n') or text.endswith('\r\n'):
                self.jianer_setup_apply.console_log.append("")
                
            # 自动滚动到底部
            cursor = self.jianer_setup_apply.console_log.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.jianer_setup_apply.console_log.setTextCursor(cursor)
    
    def start_bot_with_ui(self):
        """通过UI启动机器人并显示日志"""
        try:
            # 检查机器人是否已经在运行
            if self.bot_process.state() == QProcess.ProcessState.Running:
                reply = QMessageBox.question(
                    self, 
                    "机器人已在运行", 
                    "机器人当前正在运行中。\n\n是否要停止当前运行的机器人并重新启动？",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.stop_bot()
                    # 等待1秒再启动
                    QTimer.singleShot(1000, self._start_bot_delayed)
                return
            
            # 启动机器人
            self._start_bot_delayed()
            
        except Exception as e:
            self.append_log_error(f"启动机器人失败: {str(e)}\n")
    
    def _start_bot_delayed(self):
        """延迟启动机器人"""
        try:
            self.append_log_output("正在启动机器人...\n")
            
            # 更改按钮文本
            self.jianer_setup_apply.PrimaryPushButton_2.setText("停止机器人")
            self.jianer_setup_apply.PrimaryPushButton_2.clicked.disconnect()
            self.jianer_setup_apply.PrimaryPushButton_2.clicked.connect(self.stop_bot)
            
            # 启动进程
            if self.bot_process.start_bot():
                self.append_log_output("机器人启动成功，正在初始化...\n")
            else:
                self.append_log_error("机器人启动失败\n")
                self._reset_button_state()
                
        except Exception as e:
            self.append_log_error(f"启动进程出错: {str(e)}\n")
            self._reset_button_state()
    
    def stop_bot(self):
        """停止机器人"""
        try:
            if self.bot_process.state() == QProcess.ProcessState.Running:
                self.append_log_output("正在停止机器人...\n")
                self.bot_process.stop_bot()
            else:
                self.append_log_output("机器人当前未运行\n")
                self._reset_button_state()
        except Exception as e:
            self.append_log_error(f"停止机器人出错: {str(e)}\n")
    
    def on_bot_process_finished(self, exit_code):
        """机器人进程结束时的处理"""
        if exit_code == 0:
            self.append_log_output(f"机器人已正常停止 (退出码: {exit_code})\n")
        else:
            self.append_log_error(f"机器人异常停止 (退出码: {exit_code})\n")
        
        self._reset_button_state()
    
    def _reset_button_state(self):
        """重置按钮状态"""
        try:
            self.jianer_setup_apply.PrimaryPushButton_2.setText("启动机器人")
            self.jianer_setup_apply.PrimaryPushButton_2.clicked.disconnect()
            self.jianer_setup_apply.PrimaryPushButton_2.clicked.connect(self.start_bot_with_ui)
        except Exception as e:
            print(f"重置按钮状态失败: {e}")
        
    @Slot(object, object)
    def add_plugins_to_UI(self, intro_result, plugin):  # 现在是类的方法
        global local_plugins_list
        print("add " + str(plugin) + " to UI")
        if not plugin in local_plugins_list:
            IntelliMarkets.new_plugin(self.jianer_setup_plugins, plugin, intro_result['intro'])
        else:
            IntelliMarkets.new_plugin(self.jianer_setup_plugins, plugin, intro_result['intro'], False)
        self.jianer_setup_plugins.LoadingBar.setVisible(False)
        self.jianer_setup_plugins.ComboBox.setEnabled(True)
        self.jianer_setup_plugins.SearchButton.setEnabled(True)
                
    @Slot(object)
    def get_all_intro(self, plugins):
        print("Start to get all plugins intro: "+str(plugins))
        thread_pool = QThreadPool.globalInstance()
        # thread_pool.setMaxThreadCount(10)
        # self.workers = []
        for p in plugins:
            # print(p)
            try:    
                worker = TaskRunner(self.intelliMarkets.get_plugin_intro, p)
                worker.set_name(f"{p}-getting")
                worker.signals.finished.connect(lambda result, p=p: self.add_plugins_to_UI(result, p))
                thread_pool.start(worker)
            except Exception as e:
                print(f"TaskRunner 发生异常: {e}") 
            
        # thread_pool.waitForDone() # 等待所有任务完成
        
class GenerateSettings():
    global appSettings_content, config_content
        
    def gen_config(self, uin: str, host: str, port: str, gemini: str, openai: str, 
               botName: str, botNameEN: str, ROOT_User, Auto_approval: str, 
               reminder: str, Log_level: str, black_list: str, deepseek: str, slogan: str, 
               compliments: str, edge_voice: str, edge_rate: str, edge_volume: str, 
               edge_pitch: str, poke_phrases: str, default_mode: str) -> str:
        
        global config_content
        
        try:
           # 将每一行分割成列表，使用列表推导式去掉每一行可能的空白开头和结尾
            ROOT_User = ROOT_User.splitlines()
            ROOT_User_list = [line.strip() for line in ROOT_User if line.strip()]
            
            uin = uin.splitlines()
            uin_list = [line.strip() for line in uin if line.strip()]
            
            Auto_approval = Auto_approval.splitlines()
            Auto_approval_list = [line.strip() for line in Auto_approval if line.strip()]
            
            black_list = black_list.splitlines()
            black_list_list = [line.strip() for line in black_list if line.strip()]
            
            compliments = compliments.splitlines()
            compliments_list = [line.strip() for line in compliments if line.strip()]
            
            poke_phrases = poke_phrases.splitlines()
            poke_phrases_list = [line.strip() for line in poke_phrases if line.strip()]
            
            edge_settings: dict = {"voiceColor": edge_voice if edge_voice else "zh-CN-XiaoyiNeural",
              "rate": edge_rate if edge_rate else "+0%",
              "volume": edge_volume if edge_volume else "+0%",
              "pitch": edge_pitch if edge_pitch else "+0Hz"
            }
            
            match default_mode:
                case "DeepSeek (深度)":
                    default_mode = "Ds"
                case "Google Gemini (读图)":
                    default_mode = "Pixmap"
                case "ChatGPT-4 (默认4)":
                    default_mode = "Net"
                case "ChatGPT-3.5 (默认3.5)":
                    default_mode = "Normal"
                case _:
                    default_mode = "Ds"
            
            config_content = self.config(self, uin=uin_list, host=host, port=int(port), gemini=gemini, openai=openai, 
                botName=botName, botNameEN=botNameEN, ROOT_User=ROOT_User_list, Auto_approval=Auto_approval_list, 
                reminder=reminder, Log_level=Log_level, black_list=black_list_list, deepseek=deepseek, slogan=slogan, 
                compliments=compliments_list, edge_settings=edge_settings, poke_phrases=poke_phrases_list, default_mode=default_mode)
            config_content = json.dumps(config_content, indent=4, ensure_ascii=False)
            
            return config_content 
        except Exception as e:
            config_content = str(traceback.format_exc())
            return f"设置的配置有误，请核对设置清单：{str(traceback.format_exc())}"
    
    def gen_appSettings(self, uin: str, host: str, port: str, proxy: str) -> str:
        
        global appSettings_content
        
        try:
            match proxy:
                case "Master - cloudflare":
                    proxy = "https://sign.lagrangecore.org/api/sign/30366"
                case "Master - mainland":
                    proxy = "http://106.54.14.24:8084/api/sign/30366"
                case "Mirror - hk > cloudflare":
                    proxy = "https://sign.0w0.ing/api/sign/30366"
                case _:
                    proxy = ""
            
            appSettings_content = self.appSettings(uin=int(uin), proxy=proxy, host=host, port=int(port))
            appSettings_content = json.dumps(appSettings_content, indent=4, ensure_ascii=False)
            
            return appSettings_content
        except Exception as e:
            appSettings_content = str(traceback.format_exc())
            return f"设置的配置有误，请核对设置清单：{str(traceback.format_exc())}"
        
    def save_presets(self):
        global presets_content
        with open(presets_tool.CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(presets_content)
            f.close()

    def config(self, uin: list = None, host: str = "127.0.0.1", port: int = 5004, gemini: str = "", openai: str = "", 
           deepseek: str = "", botName: str = "小依", botNameEN: str = "Jianer", ROOT_User: list = None, 
           Auto_approval: list = None, reminder: str = "/", Log_level: str = "INFO", black_list: list = None, slogan: str = "", 
           compliments: list = None, edge_settings: dict = None, poke_phrases: list = None, default_mode: str = "Ds") -> dict:

        if uin is None:
            uin = []
        if ROOT_User is None:
            ROOT_User = []
        if Auto_approval is None:
            Auto_approval = []
        if black_list is None:
            black_list = []
        if compliments is None:
            compliments = []
        if poke_phrases is None:
            poke_phrases = []
            
        if edge_settings is None:
            edge_settings: dict = {"voiceColor": "zh-CN-XiaoyiNeural",
              "rate": "+0%",
              "volume": "+0%",
              "pitch": "+0Hz"
          }

        print(uin)
        return {
    "owner": uin,
    "black_list": black_list,
    "silents": [
    ],
    "Connection": {
      "mode": "FWS",
      "host": host,
      "port": port,
      "listener_host": host,
      "listener_port": 5003,
      "retries": 5,
      "satori_token": ""
    },
    "Log_level": Log_level,
    "protocol": "OneBot",
    "Others": {
      "gemini_key": gemini,
      "openai_key": openai,
      "deepseek_key": deepseek, 
      "default_mode": default_mode, 
      "bot_name": botName ,
      "bot_name_en": botNameEN,
      "ROOT_User": ROOT_User,
      "Auto_approval": Auto_approval,
      "reminder": reminder,
      "slogan": slogan, 
      "TTS": edge_settings,
      "compliment": compliments, 
      "poke_rejection_phrases": poke_phrases},
      "uin": 0
}
    
    def appSettings(uin: int, proxy: str, host: str, port: int):
        return {
    "$schema": "https://raw.githubusercontent.com/LagrangeDev/Lagrange.Core/master/Lagrange.OneBot/Resources/appsettings_schema.json",
    "Logging": {
        "LogLevel": {
            "Default": "Information",
            "Microsoft": "Warning",
            "Microsoft.Hosting.Lifetime": "Information"
        }
    },
    "SignServerUrl": proxy,
    "SignProxyUrl": "",
    "MusicSignServerUrl": "",
    "Account": {
        "Uin": uin,
        "Protocol": "Linux",
        "AutoReconnect": True,
        "GetOptimumServer": True
    },
    "Message": {
        "IgnoreSelf": True,
        "StringPost": False
    },
    "QrCode": {
        "ConsoleCompatibilityMode": False
    },
    "Implementations": [
        {
            "Type": "ForwardWebSocket",
            "Host": host,
            "Port": port,
            "HeartBeatInterval": 5000,
            "AccessToken": ""
        }
    ]
}
        
        
    def _prerequisites(self):
        global presets_content

        preset_widgets = []
        new_presets = {}
        for i in range(self.jianer_setup_pre.gridLayout.count()):
            item = self.jianer_setup_pre.gridLayout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if str(widget.objectName()).startswith("Label_Icon_") and isinstance(widget, CardWidget):
                    preset_widgets.append(widget)

        print(f"现在有的预设：{len(preset_widgets)} 个")

        for widget in preset_widgets:
            new_preset_name = str(widget.objectName()).split(r"_")[-1]
            new_presets[new_preset_name] = {}
            preset_path = f"{new_preset_name}.txt"
            new_presets[new_preset_name]["path"] = preset_path
            line_edits = widget.findChildren(LineEdit)

            for line_edit in line_edits:
                object_name = line_edit.objectName().split("-")[-1]
                match object_name:
                    case "Title":
                        new_presets[new_preset_name]["name"] = line_edit.text()
                    case "Intro":
                        new_presets[new_preset_name]["info"] = line_edit.text()
                    case "Uins":
                        new_uids = line_edit.text().strip(", ").split(", ")
                        new_presets[new_preset_name]["uid"] = [item for item in new_uids if item]

        presets_content = json.dumps(new_presets, indent=4, ensure_ascii=False)
        return presets_content

class IntelliMarkets():
    def __init__(self):
        super().__init__()
        self.g = get_github_instance(GITHUB_TOKEN, False)
        self.repo = get_repo(self.g, REPO_NAME)

    # def gen_token(self):
    #     g = get_github_instance(GITHUB_TOKEN, False)
    #     repo = get_repo(self.g, REPO_NAME)
    #     return g, repo

    def check_for_update(self, plugin_name):
        print(f"正在检查 {plugin_name} 的更新")
        if self.repo == None:
            print(f"无法连接至插件中心。")
            return False
        
        remote_paths = [
            f"{plugin_name}/{plugin_name}.py",
            f"{plugin_name}/{plugin_name}.pyw",
            f"{plugin_name}/{plugin_name}/setup.py",
            f"{plugin_name}/{plugin_name}/setup.pyw"
        ]
        
        new_content = None
        remote_path_found = None
        for remote_path in remote_paths:
            if check_file_exists(self.repo, remote_path, "main"):
                new_content = get_file_content(self.repo, remote_path, "main")
                remote_path_found = remote_path
                break
        
        if new_content is None:
            print(f"检查更新：远端不存在或未收录插件 {plugin_name}")
            return False
        
        local_name_variants = [
            plugin_name,       # 正常状态
            f"d_{plugin_name}"  # 禁用状态
        ]
        
        # 按远程路径模式确定本地查找模式
        parts = Path(remote_path_found).parts
        if len(parts) == 2:  # plugin/plugin.py 
            local_path_candidates = [
                Path(PluginsManager.PLUGIN_FOLDER) / f"{variant}{Path(remote_path_found).suffix}"
                for variant in local_name_variants
            ]
        else:  # plugin/plugin/setup.py
            local_path_candidates = [
                Path(PluginsManager.PLUGIN_FOLDER) / variant / parts[2]
                for variant in local_name_variants
            ]
        
        # 查找存在的本地文件
        local_path = None
        for candidate in local_path_candidates:
            if candidate.exists():
                local_path = candidate
                break
        
        if local_path is None:
            print(f"检查更新：本地插件 {plugin_name} 不存在或路径错误")
            return False
        
        try:
            # 计算远程哈希
            new_hash = hashlib.md5(new_content.encode('utf-8')).hexdigest()
            
            # 计算本地哈希
            with open(local_path, 'r', encoding='utf-8') as f:
                local_hash = hashlib.md5(f.read().encode('utf-8')).hexdigest()
            
            return new_hash != local_hash
        except UnicodeDecodeError:
            print(f"检查更新：插件 {plugin_name} 编码不是 UTF-8")
            return False
        except Exception as e:
            print(f"检查更新：读取插件 {plugin_name} 时出错: {str(e)}")
            return False

    def get_all_plugins(self) -> list:
        print("get plugins")
        try:
            lst = get_folder_list(self.repo, branch="main")
            print("list getted")
            return lst
        except:
            self.jianer_setup_plugins.ComboBox.setEnabled(True)
            self.jianer_setup_plugins.SearchButton.setEnabled(True)
            InfoBar.warning(
                title='插件中心连接失败',
                content="请检查 Github 连接状态，使用代理可能解决此问题。\n请重新选择筛选条件以刷新插件中心。",
                orient=Qt.Horizontal,
                isClosable=True,   # enable close button
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self
            )
            return []
        
    def pre_install_plugin(self, p_name, is_update=False):
        global plugin_installing
        if plugin_installing:
            InfoBar.warning(
                title='请稍后再试',
                content="当前有一个插件正在安装 _(:з」∠)_",
                orient=Qt.Horizontal,
                isClosable=True,   # enable close button
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=2000,
                parent=self
            )
            return
        
        if not is_update:
            w = MessageBox(f"即将安装插件：{p_name}", f'''请确保您已详细阅读其介绍和开源协议，并清楚插件会对你的机器人造成的改变。
简儿开发团队不对任何因插件造成的任何后果负责，如有问题，请第一时间联系插件开发人员。''', self)
        else:
            w = MessageBox(f"即将更新插件：{p_name}", f'''若安装顺利，你的插件数据不会有任何丢失。''', self)
        if w.exec():
            plugin_installing = True
            self.stateTooltip = StateToolTip('正在安装插件', '请耐心等待哦 (๑•̀ㅂ•́)و✧', self)
            self.stateTooltip.move(30, 30)
            self.stateTooltip.show()
            self.LoadingBar.setVisible(True)
            
            worker = TaskRunner(IntelliMarkets.install_plugin, self, p_name)
            worker.set_name(name=f"{p_name}-installing")
            worker.signals.finished.connect(lambda result, s=self: IntelliMarkets.finishied_install_plugin(s, result))
            QThreadPool.globalInstance().start(worker)

    @Slot(object)
    def finishied_install_plugin(self, r):
        print("安装完成")
        self.stateTooltip.setContent('插件安装完成啦 (*≧ω≦)')
        self.stateTooltip.setState(True)
        self.stateTooltip = None
        self.LoadingBar.setVisible(False)
        
        w = MessageBox(f"安装结束", r, self)
        w.exec()
        InfoBar.success(
                title='刷新以显示',
                content="请重新选择筛选条件以刷新插件中心 ~o( =∩ω∩= )m",
                orient=Qt.Horizontal,
                isClosable=True,   # enable close button
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=5000,
                parent=self
            )
        
        global plugin_installing
        plugin_installing = False

    def install_plugin(self, plugin_name) -> str:
        global plugins_list
        self.repo = get_repo(get_github_instance(GITHUB_TOKEN, False), REPO_NAME)
        try:
            plugin_data = plugins_list.get(plugin_name)
            if not plugin_data:
                raise ValueError(f"插件 {plugin_name} 不在插件列表中")
            
            # 检查并安装依赖
            print("检查并安装依赖")
            if plugin_data.get('depend'):
                if "没有相关依赖" not in plugin_data['depend']:
                    if len(getproxies()) > 0:
                        print("warn: 本地已连接代理，不使用 pip 包镜像。")
                        IntelliMarkets.install_requirements(self, plugin_data['depend'])
                    else:
                        IntelliMarkets.install_requirements(self, plugin_data['depend'], "https://pypi.tuna.tsinghua.edu.cn/simple")
            
            # 尝试不同文件类型
            plugin_files = [
                (f"{plugin_name}/{plugin_name}.py", f"{plugin_name}.py"),
                (f"{plugin_name}/{plugin_name}.pyw", f"{plugin_name}.pyw"),
            ]
            
            for remote_path, local_name in plugin_files:
                if check_file_exists(self.repo, remote_path, "main"):
                    print("开始安装")
                    content = get_file_content(self.repo, remote_path, "main")
                    target_path = Path(PluginsManager.PLUGIN_FOLDER) / local_name
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with target_path.open("w", encoding='utf-8') as f:
                        f.write(content)
                    return f"{plugin_name} 已成功安装到你的简儿中 o((>ω< ))o"
            
            # 检查是否是包格式插件
            setup_files = [
                f"{plugin_name}/{plugin_name}/setup.py",
                f"{plugin_name}/{plugin_name}/setup.pyw"
            ]
            
            print("开始安装")
            for setup_file in setup_files:
                if check_file_exists(self.repo, setup_file, "main"):
                    # target_dir = Path(PluginsManager.PLUGIN_FOLDER) / plugin_name
                    download_folder(self.repo, f"{plugin_name}/{plugin_name}", PluginsManager.PLUGIN_FOLDER, "main")
                    return f"{plugin_name} 已成功安装到你的简儿中 o((>ω< ))o"
            
            raise FileNotFoundError(f"远端不存在或未收录插件 {plugin_name}")
            
        except subprocess.CalledProcessError as e:
            return f"安装过程中发生错误: \n依赖安装失败: {str(e)}\n\n插件未能完成安装 (っ °Д °;)っ"
        except FileNotFoundError as e:
            return f"安装过程中发生错误: \n找不到插件文件: {str(e)}\n\n插件未能完成安装 (っ °Д °;)っ"
        except Exception as e:
            error_msg = f"安装过程中发生错误: \n{str(e)}\n\n插件未能完成安装 (っ °Д °;)っ"
            print(f"{error_msg}\n{traceback.format_exc()}") 
            return error_msg

    def install_requirements(self, requirements_content: str, index_url: Optional[str] = None, timeout: int = 300):
        if not requirements_content.strip():
            return True

        valid_lines = [
            line.strip() for line in requirements_content.splitlines()
            if line.strip() and not line.startswith("#")
        ]
        if not valid_lines:
            return True

        # 临时目录
        with tempfile.TemporaryDirectory() as tmpdir:
            req_file = Path(tmpdir) / "requirements.txt"
            req_file.write_text("\n".join(valid_lines))
            
            command = [
                sys.executable, "-m", "pip", "install",
                "-r", str(req_file),
                "--disable-pip-version-check",
                "--no-warn-script-location"
            ]
            if index_url:
                command.extend(["-i", index_url])
                if index_url:
                    command.extend(["--trusted-host", index_url])
            
            try:
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,  #合并输出
                    timeout=timeout,
                    check=True,
                    text=True
                )
                print(f"依赖安装成功: {result.stdout}")
                return True
            except subprocess.TimeoutExpired:
                raise RuntimeError("依赖安装超时")
            except subprocess.CalledProcessError as e:
                error_msg = f"{e.stdout}"
                print(error_msg)
                raise RuntimeError(error_msg)
            except Exception as e:
                print(f"{e}")
                raise
                
    def remove_plugin(self, p_name):
        w = MessageBox(f"即将删除插件：{p_name}", f'''在你最终做好决策之前，请不要点击确认按钮，否则该插件及其数据将会被立即删除。''', self)
        if w.exec():
            try:
                base_path = os.path.abspath(os.path.join(PluginsManager.PLUGIN_FOLDER, p_name))
                d_base_path = os.path.abspath(os.path.join(PluginsManager.PLUGIN_FOLDER, f"d_{p_name}"))
                plugin_paths = [
                    base_path, 
                    f"{base_path}.py",
                    f"{base_path}.pyw",
                    d_base_path,
                    f"{d_base_path}.py",
                    f"{d_base_path}.pyw",
                ]
                
                for path in plugin_paths:
                    if os.path.isdir(path):
                        shutil.rmtree(path)  # 递归删除目录
                    elif os.path.isfile(path):
                        os.remove(path)
                        
                # o = self.ComboBox.currentIndex()
                # self.ComboBox.setCurrentIndex(2)
                # self.ComboBox.setCirrentIndex(o)
                wx = MessageBox(f"删除完毕", f"插件 {p_name} 已成功从你的机器人中删除，感谢您使用此插件。", self)
                wx.exec()
            except Exception as e:
                print(traceback.format_exc())
                wx = MessageBox(f"删除完毕", f"删除插件时发生错误：\n{e}\n\n该插件可能未能彻底从你的机器人中删除", self)
                wx.exec()
            finally:
                InfoBar.success(
                    title='刷新以显示',
                    content="请重新选择筛选条件以刷新插件中心 ~o( =∩ω∩= )m",
                    orient=Qt.Horizontal,
                    isClosable=True,   # enable close button
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=5000,
                    parent=self
                )

    def get_plugin_intro(self, list) -> dict:
        # intro_list = []
        # for plugin in list:
        #     path = f"{str(plugin)}/README.md"
        #     if check_file_exists(self.repo, path, "main"):
        #         intro_list.append(str(get_file_content(self.repo, path, "main")))
        #     else:
        #         intro_list.append("没有相关介绍 (README.md)")

        # return intro_list
        print("寻找intro: "+list)
        global plugins_list
        info = {}
        
        path = f"{str(list)}/README.md"
        if check_file_exists(self.repo, path, "main"):
            info['intro'] = str(get_file_content(self.repo, path, "main"))
        else:
            info['intro'] = "没有相关介绍 (README.md)"
        
        path = f"{str(list)}/requirements.txt"
        if check_file_exists(self.repo, path, "main"):
            info['depend'] = str(get_file_content(self.repo, path, "main"))
        else:
            info['depend'] = "没有相关依赖 (requirements.txt)"
        
        path = f"{str(list)}/LICENSE"
        if check_file_exists(self.repo, path, "main"):
            info['agreement'] = str(get_file_content(self.repo, path, "main"))
        else:
            path = f"{str(list)}/LICENSE.txt"
            if check_file_exists(self.repo, path, "main"):
                info['agreement'] = str(get_file_content(self.repo, path, "main"))
            else:
                info['agreement'] = "没有相关协议 (LICENSE)"
                
        plugins_list[str(list)] = info
        print("寻找完成")
        return info
        
        
    def show_plugin_window(self, p):
        global plugins_list
        dialog = JianerSetupPluginWindow(self, is_dark_mode=isDarkTheme())  # 创建对话框传递父窗口
        # dialog.updateContent(title="My Plugin", intro="This is a great plugin!", depend="PySide6, requests", licence="MIT")
        if p in plugins_list and plugins_list[p]:
            dialog.updateContent(p, plugins_list[p]['intro'], plugins_list[p]['depend'], plugins_list[p]['agreement'])
        else:
            dialog.updateContent(p)

        result = dialog.exec()
        if result == QDialog.Accepted:
            print("Dialog accepted")
        else:
            print("Dialog rejected")
            
    def check_plugin_state(self, plugin_name: str) -> bool:
        base_path = Path(PluginsManager.PLUGIN_FOLDER)

        possible_names = [
            f"d_{plugin_name}.py",
            f"d_{plugin_name}.pyw",
            f"d_{plugin_name}"]
        
        # 检查是否存在任何禁用标记
        for name in possible_names:
            if (base_path / name).exists():
                return False # 禁用了
        
        return True #启用了
    
    def set_plugin_state(self, name: str) -> str:
        base = Path(PluginsManager.PLUGIN_FOLDER)
        disable = False if IntelliMarkets.check_plugin_state(self, name) else True
        
        for prefix in ["", "d_"]:
            for suffix in ["", ".py", ".pyw"]:
                path = base / f"{prefix}{name}{suffix}"
                print(str(path))
                if path.exists():
                    new_prefix = "d_" if not disable else ""
                    new_path = base / f"{new_prefix}{name}{suffix}"
                    print(f"new {str(new_path)}")
                    if path != new_path:  # 不是目标状态
                        try:
                            path.rename(new_path)
                            InfoBar.success(
                                title='已设置插件',
                                content=f"插件 {name} 已{'启用' if disable else '禁用'}成功 ⌯>ᴗo⌯ .ᐟ.ᐟ",
                                orient=Qt.Horizontal,
                                isClosable=True,   # enable close button
                                position=InfoBarPosition.BOTTOM_RIGHT,
                                duration=2000,
                                parent=self
                            )
                            return '禁用' if disable else '启用'
                        except OSError:
                            InfoBar.error(
                                title='无法设置插件',
                                content="请求的操作被拒绝访问。",
                                orient=Qt.Horizontal,
                                isClosable=True,   # enable close button
                                position=InfoBarPosition.BOTTOM_RIGHT,
                                duration=2000,
                                parent=self
                            )
                            return '启用' if disable else '禁用'
                    else:
                        InfoBar.success(
                            title='已设置插件',
                            content=f"插件 {name} 已{'禁用' if disable else '启用'}成功 ⌯>ᴗo⌯ .ᐟ.ᐟ",
                            orient=Qt.Horizontal,
                            isClosable=True,   # enable close button
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            duration=2000,
                            parent=self
                        )
                        return '禁用' if disable else '启用'
                        
        InfoBar.error(
            title='无法设置插件',
            content="找不到该插件文件 ヾ( ･`⌓´･)ﾉﾞ",
            orient=Qt.Horizontal,
            isClosable=True,   # enable close button
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self
        )
        return '启用' if disable else '禁用'
        
    def new_plugin(self, plugins_name, plugins_intro = "没有相关介绍 (README.md)", is_all = True, is_to_update = False):
        global plugins_num

        # 防止切换页面后意外地添加插件
        if ((self.ComboBox.currentIndex() == 0 and is_to_update) or # Except: is_all == True, is_to_update == False
            (self.ComboBox.currentIndex() == 1 and (is_all or is_to_update)) or # Except: is_all == False, is_to_update == False
            (self.ComboBox.currentIndex() == 2 and (is_all or not is_to_update))): # Except: is_all == False, is_to_update == True
            print(
                f"add UI force closed because of currentIndex == {str(self.ComboBox.currentIndex())} and is_all == {str(is_all)}, is_to_update == {str(is_to_update)}")
            return 
        
        print("add new plugin")
        self.Label_Plugin_ = CardWidget(self.scrollAreaWidgetContents)
        self.Label_Plugin_.setObjectName(f"Label_Plugin_{plugins_name}")
        self.Label_Plugin_.setMinimumSize(QSize(0, 138))
        self.Label_Plugin_.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_9 = QHBoxLayout(self.Label_Plugin_)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_23 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_23)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_25 = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_9.addItem(self.verticalSpacer_25)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.PluginTitle = TitleLabel(self.Label_Plugin_)
        self.PluginTitle.setObjectName(u"PluginTitle")

        self.horizontalLayout_3.addWidget(self.PluginTitle)
        self.verticalLayout_9.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_27 = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_9.addItem(self.verticalSpacer_27)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)

        self.PluginIntro = StrongBodyLabel(self.Label_Plugin_)
        self.PluginIntro.setObjectName(u"PluginIntro")
        self.PluginIntro.setWordWrap(True)
        self.PluginIntro.adjustSize()
        self.PluginIntro.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout_5.addWidget(self.PluginIntro)

        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_11)

        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_28 = QSpacerItem(20, 4, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_9.addItem(self.verticalSpacer_28)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_5 = QSpacerItem(178, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        if not is_all:
            self.AblitilyButton = PushButton(self.Label_Plugin_)
            self.AblitilyButton.setObjectName(u"AblitilyButton")
            
            self.AblitilyButton.clicked.connect(lambda self=self, n=plugins_name: self.AblitilyButton.setText(IntelliMarkets.set_plugin_state(self, n)))

            self.horizontalLayout_6.addWidget(self.AblitilyButton)

        self.ManageButton = PushButton(self.Label_Plugin_)
        self.ManageButton.setObjectName(u"ManageButton")
        
        if (is_all and not is_to_update) or (not is_all and is_to_update):
            self.ManageButton.clicked.connect(lambda :IntelliMarkets.pre_install_plugin(self, plugins_name, is_to_update))
        else:
            self.ManageButton.clicked.connect(lambda: IntelliMarkets.remove_plugin(self, plugins_name))

        self.horizontalLayout_6.addWidget(self.ManageButton)

        self.InfoButton = PrimaryPushButton(self.Label_Plugin_)
        self.InfoButton.setObjectName(u"InfoButton")
        self.InfoButton.clicked.connect(lambda: IntelliMarkets.show_plugin_window(self, plugins_name))
        
        self.horizontalLayout_6.addWidget(self.InfoButton)
        self.horizontalSpacer_6 = QSpacerItem(5, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.verticalSpacer_29 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_9.addItem(self.verticalSpacer_29)
        self.horizontalLayout_9.addLayout(self.verticalLayout_9)
        self.horizontalSpacer_24 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(self.horizontalSpacer_24)

        self.gridLayout.addWidget(self.Label_Plugin_, 4 + plugins_num, 0, 1, 1)
        plugins_num += 1
        
        lines = str(plugins_intro).splitlines() 
        if len(lines) > 2:
            plugins_intro = '\n'.join(lines[:2]) + "……"

        self.PluginTitle.setText(QCoreApplication.translate("Form", plugins_name, None))
        self.PluginIntro.setText(QCoreApplication.translate("Form", plugins_intro, None))
        if not is_all: self.AblitilyButton.setText(QCoreApplication.translate("Form", 
            "禁用" if IntelliMarkets.check_plugin_state(self, plugins_name) else "启用", None))

        M_buttonText = u"\u5b89\u88c5"
        if is_all:
            pass
        elif not is_all and is_to_update:
            M_buttonText = "更新"
        elif not is_all and not is_to_update:
            M_buttonText = "删除"
        self.ManageButton.setText(QCoreApplication.translate("Form", M_buttonText, None))
        self.InfoButton.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u66f4\u591a\u4fe1\u606f", None))
        
    def del_all_plugin_UI(self):
        global plugins_num

        # print(self.gridLayout.count())
        for i in reversed(range(self.gridLayout.count())): # 倒序遍历
            item = self.gridLayout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if str(widget.objectName()).startswith("Label_Plugin_"):
                    self.gridLayout.removeItem(item)
                    widget.setParent(None)

        plugins_num = 0
                
        #         girl_friend = self.validate_and_format(self, n)
#         sister = self.validate_and_format(self, s)
#         Ju_Heqiu = self.validate_and_format(self, j)
        
#         return f'''class prerequisite:
#     def __init__(self, bot_name: str, event_user: str):
#         self.bot_name = bot_name
#         self.event_user = event_user
        
#     def mother(self) -> str:
#         return f"""{Ju_Heqiu}"""

#     def girl_friend(self) -> str:
#         return f"""{girl_friend}"""

#     def sister(self) -> str:
#         return f"""{sister}"""
        
# '''
        
if __name__ == '__main__':
    # 设置高DPI缩放策略（PySide6中不再需要手动设置AA_EnableHighDpiScaling和AA_UseHighDpiPixmaps）
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # 设置跟随系统主题和主题色
    setTheme(Theme.AUTO)
    setThemeColor("#e9adb0")
    
    app = Application(sys.argv)
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--run-bot':
        # 直接运行机器人，不显示UI
        print("正在启动简儿QQ机器人...")
        try:
            # 导入并运行主程序
            import main
        except Exception as e:
            print(f"启动机器人失败: {e}")
            sys.exit(1)
    else:
        # 正常启动配置向导
        t = FluentTranslator()
        app.installTranslator(t)
        
        w = SetupWizard()
        w.show()
        app.exec()    
    
