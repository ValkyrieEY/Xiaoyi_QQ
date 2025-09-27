from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import (SplitFluentWindow, FluentIcon, 
                            NavigationItemPosition, CardWidget, LineEdit, PrimaryPushButton, PushButton, SubtitleLabel, 
                            FluentTranslator, Theme, setTheme, setThemeColor, isDarkTheme, 
                            SplashScreen, MessageBox, TitleLabel, StrongBodyLabel)

from wizardWindows import JianerSetupWizard_rc
from wizardWindows.Ui_JianerSetupAbout import Ui_Form as Ui_JianerSetupAbout
from wizardWindows.Ui_JianerSetupAdvanced import Ui_Form as Ui_JianerSetupAdvanced
from wizardWindows.Ui_JianerSetupAI import Ui_Form as Ui_JianerSetupAI
from wizardWindows.Ui_JianerSetupApply import Ui_Form as Ui_JianerSetupApply
from wizardWindows.Ui_JianerSetupBasic import Ui_Form as Ui_JianerSetupBasic
from wizardWindows.Ui_JianerSetupLgr import Ui_Form as Ui_JianerSetupLgr
from wizardWindows.Ui_JianerSetupPre import Ui_Form as Ui_JianerSetupPre
from wizardWindows.Ui_JianerSetupWizard import Ui_Form as Ui_JianerSetupWizard
from wizardWindows.Ui_JianerSetupOthers import Ui_Form as Ui_JianerSetupOthers
from wizardWindows.Ui_JianerSetupTTS import Ui_Form as Ui_JianerSetupTTS
from wizardWindows.Ui_JianerSetupPlugins import Ui_Form as Ui_JianerSetupPlugins
from wizardWindows.Ui_JianerSetupPluginWindow import Ui_Form as Ui_JianerSetupPluginWindow
from wizardWindows.Ui_JianerSetupWorkflow import Ui_Form as Ui_JianerSetupWorkflow
from wizardWindows.Ui_JianerSetupWorkflowDialogs import RouteEditDialog, StepEditDialog
import webbrowser, os

class JianerSetupWizard(QWidget, Ui_JianerSetupWizard):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupPre(QWidget, Ui_JianerSetupPre):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.ScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupLgr(QWidget, Ui_JianerSetupLgr):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupBasic(QWidget, Ui_JianerSetupBasic):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupApply(QWidget, Ui_JianerSetupApply):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupAI(QWidget, Ui_JianerSetupAI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.IconWidget_8.setIcon(FluentIcon.MESSAGE)
        
class JianerSetupAdvanced(QWidget, Ui_JianerSetupAdvanced):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupWizard(QWidget, Ui_JianerSetupWizard):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupAbout(QWidget, Ui_JianerSetupAbout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupWizard(QWidget, Ui_JianerSetupWizard):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        self.IconWidget_2.setIcon(FluentIcon.TRANSPARENT)
        self.IconWidget.setIcon(FluentIcon.ALIGNMENT)
        self.IconWidget_3.setIcon(FluentIcon.DEVELOPER_TOOLS)
        self.IconWidget_4.setIcon(FluentIcon.PENCIL_INK)
        self.IconWidget_5.setIcon(FluentIcon.APPLICATION)
        self.IconWidget_6.setIcon(FluentIcon.CODE)
        self.IconWidget_7.setIcon(FluentIcon.CAFE)

class JianerSetupOthers(QWidget, Ui_JianerSetupOthers):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        self.IconWidget_8.setIcon(FluentIcon.CALORIES)
        self.IconWidget_2.setIcon(FluentIcon.TAG)
        self.IconWidget_9.setIcon(FluentIcon.DOWN)
        self.PokeWords.setPlainText("\n".join([
      "呜哇——！(╥﹏╥) 戳得人家头发都翘起来啦！",
      "喵嗷！(ﾟДﾟ≡ﾟдﾟ) 再戳就要炸毛了哦！",
      "噗噜噗噜~(。-`ω´-) 戳漏气了怎么办！",
      "叮！(｀へ′) 检测到非法戳戳攻击！",
      "咕叽——！(＞ｍ＜) 戳到痒痒肉了啦！",
      "哔哔！(｀ε´) 戳戳能量超标警告！",
      "咻——！(。-ω-)zzz 假装被戳睡着了...",
      "咔嗒！(￣^￣)ゞ 开启反戳戳防护罩！",
      "滴——(´-ω-｀) 今日戳戳次数已用完~",
      "嘭！(╯‵□′)╯︵┻━┻ 戳太用力散架啦！",
      "啾——！(◞‸◟ ) 再戳就哭给你看！",
      "哎呀，好疼！ ヾ(≧へ≦)〃 不要再戳了啦！"
    ]))
        self.NiceWords.setPlainText("\n".join([
      "呜哇——！(⁄ ⁄•⁄ω⁄•⁄ ⁄) 突然这么夸人家会晕过去的啦~",
      "咿呀——！(⸝⸝⸝ᵒ̴̶̷̥́ ⌑ ᵒ̴̶̷̣̥̀⸝⸝⸝) 被夸得头顶冒蒸汽了！",
      "叮铃~٩(◕‿◕｡)۶ 收到老夸奖能量充满啦！",
      "噗咻——！(//▽//) 人家要变成开心的小气球飘走了~",
      "喵嗷！(๑•́ ₃ •̀๑) 尾巴要翘起来惹~",
      "滴——(´///ω/// `) 检测到老公的甜蜜暴击！",
      "嘭嘭！(≧∇≦)ﾉ 人家的开心要像烟花一样炸开啦！",
      "呜...꒰ᐢ⸝⸝•̫•⸝⸝ᐢ꒱ 老公再说人家要变成害羞团子了..."
    ]))

class JianerSetupTTS(QWidget, Ui_JianerSetupTTS):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.SmoothScrollArea.setStyleSheet("background: transparent;")
        self.IconWidget_3.setIcon(FluentIcon.LANGUAGE)
        self.IconWidget_2.setIcon(FluentIcon.SPEED_OFF)
        self.IconWidget_4.setIcon(FluentIcon.VOLUME)
        self.IconWidget_5.setIcon(FluentIcon.SCROLL)
        
class JianerSetupPlugins(QWidget, Ui_JianerSetupPlugins):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.ScrollArea.setStyleSheet("background: transparent;")
        
class JianerSetupPluginWindow(QDialog, Ui_JianerSetupPluginWindow):
    def __init__(self, parent=None, is_dark_mode=False, is_all=True):
        super().__init__()
        self.setupUi(self)
        self.ScrollArea.setContentsMargins(0, 0, self.ScrollArea.contentsMargins().right(), self.ScrollArea.contentsMargins().bottom())
        self.ScrollArea_2.setContentsMargins(0, 0, self.ScrollArea_2.contentsMargins().right(), self.ScrollArea_2.contentsMargins().bottom())
        self.ScrollArea_3.setContentsMargins(0, 0, self.ScrollArea_3.contentsMargins().right(), self.ScrollArea_3.contentsMargins().bottom())
        
        self.DependPageText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.IntroPageText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LicencePageText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.DependPageText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.IntroPageText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LicencePageText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.IntroPageText.setStyleSheet("background: transparent;")
        if is_dark_mode:
            self.setStyleSheet("background-color: rgb(50, 50, 50);")
            self.IntroPageText.setStyleSheet("color: rgb(255, 255, 255);")
            self.DependPageText.setStyleSheet("color: rgb(255, 255, 255);")
            self.LicencePageText.setStyleSheet("color: rgb(255, 255, 255);")

        if is_all:
            pass
        
    def updateContent(self, title: str = "HelloWorld", 
                      intro: str = "没有相关介绍 (README.md)", 
                      depend: str = "没有相关依赖 (requirements.txt)", 
                      licence: str = "没有相关协议 (LICENSE)"):
        
        self.LargeTitleLabel.setText(" " + title)
        self.IntroPageText.setMarkdown(intro)
        self.DependPageText.setText(f'''该插件要求以下依赖库：
{os.linesep.join("    " + line for line in depend.splitlines() if line.strip())}'''
if not "没有相关依赖" in depend else depend)
        
        self.LicencePageText.setText(licence)
        
        self.ManageButton_2.clicked.connect(self.close)
        self.AblitilyButton_2.clicked.connect(
            lambda: webbrowser.open(f"https://github.com/IntelliMarkets/Jianer_Plugins_Index/tree/main/{title}")
        )
        self.AblitilyButton_2.setText("打开页面")
        self.ManageButton_2.setText("好")
        
        self.addSubInterface(self.IntroPage, "IntroPage", "插件介绍")
        self.addSubInterface(self.DependPage, "DependPage", "插件依赖")
        self.addSubInterface(self.LicencePage, "LicencePage", "插件开源协议")
        self.OpacityAniStackedWidget.setCurrentIndex(0)
        self.SegmentedWidget.setCurrentItem(self.IntroPage.objectName())

        self.SegmentedWidget.currentItemChanged.connect(
            lambda k:  self.OpacityAniStackedWidget.setCurrentWidget(self.OpacityAniStackedWidget.findChild(QWidget, k)))

        
    def addSubInterface(self, widget: QWidget, objectName, text):
        widget.setObjectName(objectName)
        self.OpacityAniStackedWidget.addWidget(widget)
        self.SegmentedWidget.addItem(routeKey=objectName, text=text)


class JianerSetupWorkflow(QWidget, Ui_JianerSetupWorkflow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.current_workflow = None
        self.workflow_manager = None
        
        # 连接信号
        self.setup_connections()
        
    def setup_connections(self):
        """设置信号连接"""
        # 工作流列表操作
        self.btn_new_workflow.clicked.connect(self.create_new_workflow)
        self.btn_edit_workflow.clicked.connect(self.edit_current_workflow)
        self.btn_delete_workflow.clicked.connect(self.delete_current_workflow)
        self.workflow_list.itemClicked.connect(self.on_workflow_selected)
        
        # 基本信息保存
        self.btn_save_basic.clicked.connect(self.save_basic_info)
        
        # 路由规则操作
        self.btn_add_route.clicked.connect(self.add_route)
        self.btn_edit_route.clicked.connect(self.edit_route)
        self.btn_delete_route.clicked.connect(self.delete_route)
        
        # 执行步骤操作
        self.btn_add_step.clicked.connect(self.add_step)
        self.btn_edit_step.clicked.connect(self.edit_step)
        self.btn_delete_step.clicked.connect(self.delete_step)
        self.btn_move_up.clicked.connect(self.move_step_up)
        self.btn_move_down.clicked.connect(self.move_step_down)
        
        # 测试功能
        self.btn_test_workflow.clicked.connect(self.test_workflow)
        
    def set_workflow_manager(self, workflow_manager):
        """设置工作流管理器"""
        self.workflow_manager = workflow_manager
        self.refresh_workflow_list()
        
    def refresh_workflow_list(self):
        """刷新工作流列表"""
        if not self.workflow_manager:
            return
            
        self.workflow_list.clear()
        workflows = self.workflow_manager.list_workflows()
        
        for workflow in workflows:
            from PySide6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(f"{workflow.name} ({'启用' if workflow.enabled else '禁用'})")
            item.setData(Qt.UserRole, workflow.id)
            self.workflow_list.addItem(item)
    
    def create_new_workflow(self):
        """创建新工作流"""
        if not self.workflow_manager:
            return
            
        from qfluentwidgets import MessageBox
        dialog = MessageBox("创建工作流", "请输入工作流名称：", self)
        if dialog.exec():
            name = "新工作流"  # 这里可以添加输入对话框
            try:
                workflow = self.workflow_manager.create_workflow(name, "新创建的工作流")
                self.refresh_workflow_list()
                # 选中新创建的工作流
                for i in range(self.workflow_list.count()):
                    item = self.workflow_list.item(i)
                    if item.data(Qt.UserRole) == workflow.id:
                        self.workflow_list.setCurrentItem(item)
                        self.on_workflow_selected(item)
                        break
            except Exception as e:
                MessageBox("错误", f"创建工作流失败：{e}", self).exec()
    
    def edit_current_workflow(self):
        """编辑当前工作流"""
        self.on_workflow_selected(self.workflow_list.currentItem())
    
    def delete_current_workflow(self):
        """删除当前工作流"""
        current_item = self.workflow_list.currentItem()
        if not current_item or not self.workflow_manager:
            return
            
        workflow_id = current_item.data(Qt.UserRole)
        from qfluentwidgets import MessageBox
        
        dialog = MessageBox("确认删除", "确定要删除这个工作流吗？此操作不可恢复。", self)
        if dialog.exec():
            try:
                self.workflow_manager.delete_workflow(workflow_id)
                self.refresh_workflow_list()
                self.clear_workflow_details()
            except Exception as e:
                MessageBox("错误", f"删除工作流失败：{e}", self).exec()
    
    def on_workflow_selected(self, item):
        """工作流被选中时"""
        if not item or not self.workflow_manager:
            return
            
        workflow_id = item.data(Qt.UserRole)
        self.current_workflow = self.workflow_manager.get_workflow(workflow_id)
        
        if self.current_workflow:
            self.load_workflow_details()
    
    def load_workflow_details(self):
        """加载工作流详细信息"""
        if not self.current_workflow:
            return
            
        # 加载基本信息
        self.LineEdit_name.setText(self.current_workflow.name)
        self.TextEdit_desc.setText(self.current_workflow.description)
        self.SwitchButton_enabled.setChecked(self.current_workflow.enabled)
        
        # 加载路由规则
        self.refresh_routes_list()
        
        # 加载执行步骤
        self.refresh_steps_list()
    
    def clear_workflow_details(self):
        """清空工作流详情"""
        self.current_workflow = None
        self.LineEdit_name.clear()
        self.TextEdit_desc.clear()
        self.SwitchButton_enabled.setChecked(False)
        self.routes_list.clear()
        self.steps_list.clear()
        self.TextEdit_test_result.clear()
    
    def save_basic_info(self):
        """保存基本信息"""
        if not self.current_workflow or not self.workflow_manager:
            return
            
        try:
            self.current_workflow.name = self.LineEdit_name.text()
            self.current_workflow.description = self.TextEdit_desc.toPlainText()
            self.current_workflow.enabled = self.SwitchButton_enabled.isChecked()
            
            self.workflow_manager.save_workflow(self.current_workflow)
            self.refresh_workflow_list()
            
            from qfluentwidgets import InfoBar, InfoBarPosition
            InfoBar.success(
                title='保存成功',
                content="工作流基本信息已保存",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        except Exception as e:
            from qfluentwidgets import MessageBox
            MessageBox("错误", f"保存失败：{e}", self).exec()
    
    def refresh_routes_list(self):
        """刷新路由规则列表"""
        self.routes_list.clear()
        if not self.current_workflow:
            return
            
        for i, route in enumerate(self.current_workflow.routes):
            from PySide6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(f"{route.name} ({route.rule_type.value}) - {'启用' if route.enabled else '禁用'}")
            item.setData(Qt.UserRole, i)
            self.routes_list.addItem(item)
    
    def add_route(self):
        """添加路由规则"""
        dialog = RouteEditDialog(self)
        if dialog.exec():
            route_data = dialog.get_route_data()
            if route_data['name']:
                try:
                    from Tools.workflow_manager import WorkflowRoute, RoutingRule
                    import uuid
                    
                    route = WorkflowRoute(
                        id=str(uuid.uuid4()),
                        name=route_data['name'],
                        rule_type=RoutingRule(route_data['rule_type']),
                        condition=route_data['condition'],
                        priority=route_data['priority'],
                        enabled=route_data['enabled'],
                        description=route_data['description']
                    )
                    
                    self.current_workflow.routes.append(route)
                    self.refresh_routes_list()
                except Exception as e:
                    from qfluentwidgets import MessageBox
                    MessageBox("错误", f"添加路由失败：{e}", self).exec()
    
    def edit_route(self):
        """编辑路由规则"""
        current_item = self.routes_list.currentItem()
        if not current_item or not self.current_workflow:
            return
            
        route_index = current_item.data(Qt.UserRole)
        route = self.current_workflow.routes[route_index]
        
        route_data = {
            'name': route.name,
            'rule_type': route.rule_type.value,
            'condition': route.condition,
            'priority': route.priority,
            'enabled': route.enabled,
            'description': route.description
        }
        
        dialog = RouteEditDialog(self, route_data)
        if dialog.exec():
            new_data = dialog.get_route_data()
            if new_data['name']:
                try:
                    from Tools.workflow_manager import RoutingRule
                    
                    route.name = new_data['name']
                    route.rule_type = RoutingRule(new_data['rule_type'])
                    route.condition = new_data['condition']
                    route.priority = new_data['priority']
                    route.enabled = new_data['enabled']
                    route.description = new_data['description']
                    
                    self.refresh_routes_list()
                except Exception as e:
                    from qfluentwidgets import MessageBox
                    MessageBox("错误", f"编辑路由失败：{e}", self).exec()
    
    def delete_route(self):
        """删除路由规则"""
        current_item = self.routes_list.currentItem()
        if not current_item or not self.current_workflow:
            return
            
        route_index = current_item.data(Qt.UserRole)
        
        from qfluentwidgets import MessageBox
        dialog = MessageBox("确认删除", "确定要删除这个路由规则吗？", self)
        if dialog.exec():
            try:
                del self.current_workflow.routes[route_index]
                self.refresh_routes_list()
            except Exception as e:
                MessageBox("错误", f"删除路由失败：{e}", self).exec()
    
    def refresh_steps_list(self):
        """刷新执行步骤列表"""
        self.steps_list.clear()
        if not self.current_workflow:
            return
            
        for i, step in enumerate(self.current_workflow.steps):
            from PySide6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(f"{i+1}. {step.name} ({step.type.value}) - {'启用' if step.enabled else '禁用'}")
            item.setData(Qt.UserRole, i)
            self.steps_list.addItem(item)
    
    def add_step(self):
        """添加执行步骤"""
        dialog = StepEditDialog(self)
        if dialog.exec():
            step_data = dialog.get_step_data()
            if step_data['name']:
                try:
                    from Tools.workflow_manager import WorkflowStep, StepType
                    import uuid
                    
                    step = WorkflowStep(
                        id=str(uuid.uuid4()),
                        name=step_data['name'],
                        type=StepType(step_data['type']),
                        config=step_data['config'],
                        enabled=step_data['enabled'],
                        description=step_data['description']
                    )
                    
                    self.current_workflow.steps.append(step)
                    self.refresh_steps_list()
                except Exception as e:
                    from qfluentwidgets import MessageBox
                    MessageBox("错误", f"添加步骤失败：{e}", self).exec()
    
    def edit_step(self):
        """编辑执行步骤"""
        current_item = self.steps_list.currentItem()
        if not current_item or not self.current_workflow:
            return
            
        step_index = current_item.data(Qt.UserRole)
        step = self.current_workflow.steps[step_index]
        
        step_data = {
            'name': step.name,
            'type': step.type.value,
            'config': step.config,
            'enabled': step.enabled,
            'description': step.description
        }
        
        dialog = StepEditDialog(self, step_data)
        if dialog.exec():
            new_data = dialog.get_step_data()
            if new_data['name']:
                try:
                    from Tools.workflow_manager import StepType
                    
                    step.name = new_data['name']
                    step.type = StepType(new_data['type'])
                    step.config = new_data['config']
                    step.enabled = new_data['enabled']
                    step.description = new_data['description']
                    
                    self.refresh_steps_list()
                except Exception as e:
                    from qfluentwidgets import MessageBox
                    MessageBox("错误", f"编辑步骤失败：{e}", self).exec()
    
    def delete_step(self):
        """删除执行步骤"""
        current_item = self.steps_list.currentItem()
        if not current_item or not self.current_workflow:
            return
            
        step_index = current_item.data(Qt.UserRole)
        
        from qfluentwidgets import MessageBox
        dialog = MessageBox("确认删除", "确定要删除这个执行步骤吗？", self)
        if dialog.exec():
            try:
                del self.current_workflow.steps[step_index]
                self.refresh_steps_list()
            except Exception as e:
                MessageBox("错误", f"删除步骤失败：{e}", self).exec()
    
    def move_step_up(self):
        """上移步骤"""
        current_item = self.steps_list.currentItem()
        if not current_item or not self.current_workflow:
            return
            
        step_index = current_item.data(Qt.UserRole)
        if step_index > 0:
            steps = self.current_workflow.steps
            steps[step_index], steps[step_index-1] = steps[step_index-1], steps[step_index]
            self.refresh_steps_list()
            self.steps_list.setCurrentRow(step_index - 1)
    
    def move_step_down(self):
        """下移步骤"""
        current_item = self.steps_list.currentItem()
        if not current_item or not self.current_workflow:
            return
            
        step_index = current_item.data(Qt.UserRole)
        if step_index < len(self.current_workflow.steps) - 1:
            steps = self.current_workflow.steps
            steps[step_index], steps[step_index+1] = steps[step_index+1], steps[step_index]
            self.refresh_steps_list()
            self.steps_list.setCurrentRow(step_index + 1)
    
    def test_workflow(self):
        """测试工作流"""
        if not self.current_workflow or not self.workflow_manager:
            return
            
        test_message = self.TextEdit_test_message.toPlainText().strip()
        if not test_message:
            from qfluentwidgets import MessageBox
            MessageBox("提示", "请输入测试消息", self).exec()
            return
            
        try:
            # 模拟消息上下文
            message_context = {
                'message': test_message,
                'user_id': '123456',
                'group_id': '789012',
                'user_permissions': ['USER'],
                'actions': None  # 测试时不需要真实的actions
            }
            
            # 创建执行器并测试
            from Tools.workflow_manager import WorkflowExecutor
            executor = WorkflowExecutor(self.workflow_manager, [])
            
            # 异步执行需要使用事件循环
            import asyncio
            
            async def run_test():
                result = await executor.execute_workflow(self.current_workflow.id, message_context)
                return result
            
            # 在主线程中执行异步任务
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_test())
            loop.close()
            
            # 显示测试结果
            result_text = f"测试完成\n结果：{'成功' if result else '失败'}\n\n执行日志：\n"
            if hasattr(executor, 'active_executions') and executor.active_executions:
                for context in executor.active_executions.values():
                    result_text += "\n".join(context.logs)
                    break
            
            self.TextEdit_test_result.setText(result_text)
            
        except Exception as e:
            self.TextEdit_test_result.setText(f"测试出错：{e}\n\n{traceback.format_exc()}")