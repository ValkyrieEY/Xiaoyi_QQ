# -*- coding: utf-8 -*-

################################################################################
## Form generated for XIAOYI Workflow Setup UI
##
## Created for: XIAOYI QQ Bot Workflow Management
##
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QTabWidget,
    QListWidget, QListWidgetItem, QSplitter)

from qfluentwidgets import (CardWidget, ComboBox, LargeTitleLabel,
    LineEdit, PopUpAniStackedWidget, PrimaryPushButton, PushButton,
    ScrollArea, StrongBodyLabel, SubtitleLabel, TitleLabel,
    ToolButton, PlainTextEdit, CheckBox, SpinBox, TextEdit,
    TreeWidget, TableWidget, SplitPushButton, TogglePushButton,
    InfoBar, MessageBox, Slider, SwitchButton)
from wizardWindows import JianerSetupWizard_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 750)
        Form.setMinimumSize(QSize(800, 600))
        
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
        # 主要内容区域
        self.PopUpAniStackedWidget = PopUpAniStackedWidget(Form)
        self.PopUpAniStackedWidget.setObjectName(u"PopUpAniStackedWidget")
        
        # 主页面
        self.page = QWidget()
        self.page.setObjectName(u"page")
        
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # 顶部间距
        self.verticalSpacer_top = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(self.verticalSpacer_top)
        
        # 标题区域
        self.header_widget = QWidget(self.page)
        self.header_widget.setMaximumSize(QSize(16777215, 100))
        self.header_widget.setObjectName(u"header_widget")
        
        self.header_layout = QVBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(40, 0, 40, 0)
        self.header_layout.setObjectName(u"header_layout")
        
        self.LargeTitleLabel = LargeTitleLabel(self.header_widget)
        self.LargeTitleLabel.setObjectName(u"LargeTitleLabel")
        self.header_layout.addWidget(self.LargeTitleLabel)
        
        self.SubtitleLabel_main = SubtitleLabel(self.header_widget)
        self.SubtitleLabel_main.setObjectName(u"SubtitleLabel_main")
        self.header_layout.addWidget(self.SubtitleLabel_main)
        
        self.verticalLayout.addWidget(self.header_widget)
        
        # 主内容区域 - 使用分割器
        self.main_splitter = QSplitter(Qt.Horizontal, self.page)
        self.main_splitter.setObjectName(u"main_splitter")
        
        # 左侧工作流列表
        self.left_panel = CardWidget(self.main_splitter)
        self.left_panel.setObjectName(u"left_panel")
        self.left_panel.setMinimumWidth(300)
        self.left_panel.setMaximumWidth(350)
        
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(15, 15, 15, 15)
        self.left_layout.setObjectName(u"left_layout")
        
        # 工作流列表标题和操作按钮
        self.workflow_list_header = QHBoxLayout()
        self.workflow_list_header.setObjectName(u"workflow_list_header")
        
        self.TitleLabel_workflows = TitleLabel(self.left_panel)
        self.TitleLabel_workflows.setObjectName(u"TitleLabel_workflows")
        self.workflow_list_header.addWidget(self.TitleLabel_workflows)
        
        self.workflow_list_header.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.btn_new_workflow = PushButton(self.left_panel)
        self.btn_new_workflow.setObjectName(u"btn_new_workflow")
        self.btn_new_workflow.setMaximumSize(QSize(80, 32))
        self.workflow_list_header.addWidget(self.btn_new_workflow)
        
        self.left_layout.addLayout(self.workflow_list_header)
        
        # 工作流列表
        self.workflow_list = QListWidget(self.left_panel)
        self.workflow_list.setObjectName(u"workflow_list")
        self.left_layout.addWidget(self.workflow_list)
        
        # 工作流操作按钮
        self.workflow_buttons_layout = QHBoxLayout()
        self.workflow_buttons_layout.setObjectName(u"workflow_buttons_layout")
        
        self.btn_edit_workflow = PushButton(self.left_panel)
        self.btn_edit_workflow.setObjectName(u"btn_edit_workflow")
        self.workflow_buttons_layout.addWidget(self.btn_edit_workflow)
        
        self.btn_delete_workflow = PushButton(self.left_panel)
        self.btn_delete_workflow.setObjectName(u"btn_delete_workflow")
        self.workflow_buttons_layout.addWidget(self.btn_delete_workflow)
        
        self.left_layout.addLayout(self.workflow_buttons_layout)
        
        self.main_splitter.addWidget(self.left_panel)
        
        # 右侧详情区域
        self.right_panel = CardWidget(self.main_splitter)
        self.right_panel.setObjectName(u"right_panel")
        
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(15, 15, 15, 15)
        self.right_layout.setObjectName(u"right_layout")
        
        # 工作流详情标签页
        self.workflow_tabs = QTabWidget(self.right_panel)
        self.workflow_tabs.setObjectName(u"workflow_tabs")
        
        # 基本信息标签页
        self.tab_basic = QWidget()
        self.tab_basic.setObjectName(u"tab_basic")
        
        self.basic_scroll = ScrollArea(self.tab_basic)
        self.basic_scroll.setObjectName(u"basic_scroll")
        self.basic_scroll.setWidgetResizable(True)
        
        self.basic_content = QWidget()
        self.basic_content.setObjectName(u"basic_content")
        
        self.basic_layout = QVBoxLayout(self.basic_content)
        self.basic_layout.setContentsMargins(20, 20, 20, 20)
        self.basic_layout.setObjectName(u"basic_layout")
        
        # 工作流名称
        self.workflow_name_card = CardWidget(self.basic_content)
        self.workflow_name_card.setObjectName(u"workflow_name_card")
        
        self.workflow_name_layout = QVBoxLayout(self.workflow_name_card)
        self.workflow_name_layout.setContentsMargins(15, 15, 15, 15)
        
        self.TitleLabel_name = TitleLabel(self.workflow_name_card)
        self.TitleLabel_name.setObjectName(u"TitleLabel_name")
        self.workflow_name_layout.addWidget(self.TitleLabel_name)
        
        self.LineEdit_name = LineEdit(self.workflow_name_card)
        self.LineEdit_name.setObjectName(u"LineEdit_name")
        self.workflow_name_layout.addWidget(self.LineEdit_name)
        
        self.basic_layout.addWidget(self.workflow_name_card)
        
        # 工作流描述
        self.workflow_desc_card = CardWidget(self.basic_content)
        self.workflow_desc_card.setObjectName(u"workflow_desc_card")
        
        self.workflow_desc_layout = QVBoxLayout(self.workflow_desc_card)
        self.workflow_desc_layout.setContentsMargins(15, 15, 15, 15)
        
        self.TitleLabel_desc = TitleLabel(self.workflow_desc_card)
        self.TitleLabel_desc.setObjectName(u"TitleLabel_desc")
        self.workflow_desc_layout.addWidget(self.TitleLabel_desc)
        
        self.TextEdit_desc = TextEdit(self.workflow_desc_card)
        self.TextEdit_desc.setObjectName(u"TextEdit_desc")
        self.TextEdit_desc.setMaximumHeight(100)
        self.workflow_desc_layout.addWidget(self.TextEdit_desc)
        
        self.basic_layout.addWidget(self.workflow_desc_card)
        
        # 工作流状态
        self.workflow_status_card = CardWidget(self.basic_content)
        self.workflow_status_card.setObjectName(u"workflow_status_card")
        
        self.workflow_status_layout = QHBoxLayout(self.workflow_status_card)
        self.workflow_status_layout.setContentsMargins(15, 15, 15, 15)
        
        self.TitleLabel_enabled = TitleLabel(self.workflow_status_card)
        self.TitleLabel_enabled.setObjectName(u"TitleLabel_enabled")
        self.workflow_status_layout.addWidget(self.TitleLabel_enabled)
        
        self.workflow_status_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.SwitchButton_enabled = SwitchButton(self.workflow_status_card)
        self.SwitchButton_enabled.setObjectName(u"SwitchButton_enabled")
        self.workflow_status_layout.addWidget(self.SwitchButton_enabled)
        
        self.basic_layout.addWidget(self.workflow_status_card)
        
        # 保存按钮
        self.save_button_layout = QHBoxLayout()
        self.save_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.btn_save_basic = PrimaryPushButton(self.basic_content)
        self.btn_save_basic.setObjectName(u"btn_save_basic")
        self.save_button_layout.addWidget(self.btn_save_basic)
        
        self.basic_layout.addLayout(self.save_button_layout)
        self.basic_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.basic_scroll.setWidget(self.basic_content)
        
        self.tab_basic_layout = QVBoxLayout(self.tab_basic)
        self.tab_basic_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_basic_layout.addWidget(self.basic_scroll)
        
        self.workflow_tabs.addTab(self.tab_basic, "基本信息")
        
        # 路由规则标签页
        self.tab_routes = QWidget()
        self.tab_routes.setObjectName(u"tab_routes")
        
        self.routes_layout = QVBoxLayout(self.tab_routes)
        self.routes_layout.setContentsMargins(10, 10, 10, 10)
        
        # 路由列表标题和按钮
        self.routes_header = QHBoxLayout()
        self.TitleLabel_routes = TitleLabel(self.tab_routes)
        self.TitleLabel_routes.setObjectName(u"TitleLabel_routes")
        self.routes_header.addWidget(self.TitleLabel_routes)
        
        self.routes_header.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.btn_add_route = PushButton(self.tab_routes)
        self.btn_add_route.setObjectName(u"btn_add_route")
        self.routes_header.addWidget(self.btn_add_route)
        
        self.routes_layout.addLayout(self.routes_header)
        
        # 路由列表
        self.routes_list = QListWidget(self.tab_routes)
        self.routes_list.setObjectName(u"routes_list")
        self.routes_layout.addWidget(self.routes_list)
        
        # 路由操作按钮
        self.routes_buttons = QHBoxLayout()
        self.btn_edit_route = PushButton(self.tab_routes)
        self.btn_edit_route.setObjectName(u"btn_edit_route")
        self.routes_buttons.addWidget(self.btn_edit_route)
        
        self.btn_delete_route = PushButton(self.tab_routes)
        self.btn_delete_route.setObjectName(u"btn_delete_route")
        self.routes_buttons.addWidget(self.btn_delete_route)
        
        self.routes_buttons.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.routes_layout.addLayout(self.routes_buttons)
        
        self.workflow_tabs.addTab(self.tab_routes, "路由规则")
        
        # 执行步骤标签页
        self.tab_steps = QWidget()
        self.tab_steps.setObjectName(u"tab_steps")
        
        self.steps_layout = QVBoxLayout(self.tab_steps)
        self.steps_layout.setContentsMargins(10, 10, 10, 10)
        
        # 步骤列表标题和按钮
        self.steps_header = QHBoxLayout()
        self.TitleLabel_steps = TitleLabel(self.tab_steps)
        self.TitleLabel_steps.setObjectName(u"TitleLabel_steps")
        self.steps_header.addWidget(self.TitleLabel_steps)
        
        self.steps_header.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.btn_add_step = PushButton(self.tab_steps)
        self.btn_add_step.setObjectName(u"btn_add_step")
        self.steps_header.addWidget(self.btn_add_step)
        
        self.steps_layout.addLayout(self.steps_header)
        
        # 步骤列表
        self.steps_list = QListWidget(self.tab_steps)
        self.steps_list.setObjectName(u"steps_list")
        self.steps_layout.addWidget(self.steps_list)
        
        # 步骤操作按钮
        self.steps_buttons = QHBoxLayout()
        self.btn_edit_step = PushButton(self.tab_steps)
        self.btn_edit_step.setObjectName(u"btn_edit_step")
        self.steps_buttons.addWidget(self.btn_edit_step)
        
        self.btn_delete_step = PushButton(self.tab_steps)
        self.btn_delete_step.setObjectName(u"btn_delete_step")
        self.steps_buttons.addWidget(self.btn_delete_step)
        
        self.btn_move_up = PushButton(self.tab_steps)
        self.btn_move_up.setObjectName(u"btn_move_up")
        self.steps_buttons.addWidget(self.btn_move_up)
        
        self.btn_move_down = PushButton(self.tab_steps)
        self.btn_move_down.setObjectName(u"btn_move_down")
        self.steps_buttons.addWidget(self.btn_move_down)
        
        self.steps_buttons.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.steps_layout.addLayout(self.steps_buttons)
        
        self.workflow_tabs.addTab(self.tab_steps, "执行步骤")
        
        # 测试运行标签页
        self.tab_test = QWidget()
        self.tab_test.setObjectName(u"tab_test")
        
        self.test_layout = QVBoxLayout(self.tab_test)
        self.test_layout.setContentsMargins(10, 10, 10, 10)
        
        self.TitleLabel_test = TitleLabel(self.tab_test)
        self.TitleLabel_test.setObjectName(u"TitleLabel_test")
        self.test_layout.addWidget(self.TitleLabel_test)
        
        # 测试参数输入
        self.test_input_card = CardWidget(self.tab_test)
        self.test_input_layout = QVBoxLayout(self.test_input_card)
        self.test_input_layout.setContentsMargins(15, 15, 15, 15)
        
        self.SubtitleLabel_test_input = SubtitleLabel(self.test_input_card)
        self.SubtitleLabel_test_input.setObjectName(u"SubtitleLabel_test_input")
        self.test_input_layout.addWidget(self.SubtitleLabel_test_input)
        
        self.TextEdit_test_message = TextEdit(self.test_input_card)
        self.TextEdit_test_message.setObjectName(u"TextEdit_test_message")
        self.TextEdit_test_message.setMaximumHeight(80)
        self.test_input_layout.addWidget(self.TextEdit_test_message)
        
        self.test_buttons_layout = QHBoxLayout()
        self.test_buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.btn_test_workflow = PrimaryPushButton(self.test_input_card)
        self.btn_test_workflow.setObjectName(u"btn_test_workflow")
        self.test_buttons_layout.addWidget(self.btn_test_workflow)
        
        self.test_input_layout.addLayout(self.test_buttons_layout)
        self.test_layout.addWidget(self.test_input_card)
        
        # 测试结果显示
        self.test_result_card = CardWidget(self.tab_test)
        self.test_result_layout = QVBoxLayout(self.test_result_card)
        self.test_result_layout.setContentsMargins(15, 15, 15, 15)
        
        self.SubtitleLabel_test_result = SubtitleLabel(self.test_result_card)
        self.SubtitleLabel_test_result.setObjectName(u"SubtitleLabel_test_result")
        self.test_result_layout.addWidget(self.SubtitleLabel_test_result)
        
        self.TextEdit_test_result = TextEdit(self.test_result_card)
        self.TextEdit_test_result.setObjectName(u"TextEdit_test_result")
        self.TextEdit_test_result.setReadOnly(True)
        self.test_result_layout.addWidget(self.TextEdit_test_result)
        
        self.test_layout.addWidget(self.test_result_card)
        
        self.workflow_tabs.addTab(self.tab_test, "测试运行")
        
        self.right_layout.addWidget(self.workflow_tabs)
        
        self.main_splitter.addWidget(self.right_panel)
        
        # 设置分割器比例
        self.main_splitter.setSizes([300, 700])
        
        self.verticalLayout.addWidget(self.main_splitter)
        
        # 底部间距
        self.verticalSpacer_bottom = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(self.verticalSpacer_bottom)
        
        self.PopUpAniStackedWidget.addWidget(self.page)
        self.horizontalLayout.addWidget(self.PopUpAniStackedWidget)
        
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "小依 - 工作流设置"))
        self.LargeTitleLabel.setText(_translate("Form", "工作流管理"))
        self.SubtitleLabel_main.setText(_translate("Form", "    配置和管理自动化工作流，让机器人更智能地响应用户"))
        
        self.TitleLabel_workflows.setText(_translate("Form", "工作流列表"))
        self.btn_new_workflow.setText(_translate("Form", "新建"))
        self.btn_edit_workflow.setText(_translate("Form", "编辑"))
        self.btn_delete_workflow.setText(_translate("Form", "删除"))
        
        self.TitleLabel_name.setText(_translate("Form", "工作流名称"))
        self.TitleLabel_desc.setText(_translate("Form", "工作流描述"))
        self.TitleLabel_enabled.setText(_translate("Form", "启用状态"))
        self.btn_save_basic.setText(_translate("Form", "保存基本信息"))
        
        self.TitleLabel_routes.setText(_translate("Form", "路由规则"))
        self.btn_add_route.setText(_translate("Form", "添加路由"))
        self.btn_edit_route.setText(_translate("Form", "编辑"))
        self.btn_delete_route.setText(_translate("Form", "删除"))
        
        self.TitleLabel_steps.setText(_translate("Form", "执行步骤"))
        self.btn_add_step.setText(_translate("Form", "添加步骤"))
        self.btn_edit_step.setText(_translate("Form", "编辑"))
        self.btn_delete_step.setText(_translate("Form", "删除"))
        self.btn_move_up.setText(_translate("Form", "上移"))
        self.btn_move_down.setText(_translate("Form", "下移"))
        
        self.TitleLabel_test.setText(_translate("Form", "工作流测试"))
        self.SubtitleLabel_test_input.setText(_translate("Form", "测试消息输入"))
        self.btn_test_workflow.setText(_translate("Form", "开始测试"))
        self.SubtitleLabel_test_result.setText(_translate("Form", "测试结果"))