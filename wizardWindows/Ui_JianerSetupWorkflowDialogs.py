# -*- coding: utf-8 -*-

################################################################################
## Workflow Route and Step Editor Dialogs
##
## Created for: XIAOYI QQ Bot Workflow Management
##
################################################################################

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QDialogButtonBox, QWidget, QSpacerItem, QSizePolicy)

from qfluentwidgets import (LineEdit, TextEdit, ComboBox, SpinBox, CheckBox,
    TitleLabel, SubtitleLabel, CardWidget, PrimaryPushButton, PushButton,
    PlainTextEdit, ScrollArea)


class RouteEditDialog(QDialog):
    """路由规则编辑对话框"""
    
    def __init__(self, parent=None, route_data=None):
        super().__init__(parent)
        self.route_data = route_data
        self.setupUi()
        if route_data:
            self.load_route_data(route_data)
    
    def setupUi(self):
        self.setWindowTitle("编辑路由规则")
        self.setMinimumSize(500, 400)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = TitleLabel("路由规则配置")
        layout.addWidget(title_label)
        
        # 滚动区域
        scroll_area = ScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # 基本信息卡片
        basic_card = CardWidget()
        basic_layout = QFormLayout(basic_card)
        basic_layout.setContentsMargins(20, 20, 20, 20)
        
        # 路由名称
        self.name_edit = LineEdit()
        self.name_edit.setPlaceholderText("输入路由规则名称")
        basic_layout.addRow("名称:", self.name_edit)
        
        # 路由类型
        self.type_combo = ComboBox()
        self.type_combo.addItem("关键词匹配", "keyword")
        self.type_combo.addItem("正则表达式", "regex")
        self.type_combo.addItem("用户权限", "user_permission")
        self.type_combo.addItem("群组ID", "group_id")
        self.type_combo.addItem("用户ID", "user_id")
        self.type_combo.addItem("时间条件", "time")
        self.type_combo.addItem("自定义条件", "custom")
        basic_layout.addRow("类型:", self.type_combo)
        
        # 优先级
        self.priority_spin = SpinBox()
        self.priority_spin.setRange(0, 1000)
        self.priority_spin.setValue(100)
        basic_layout.addRow("优先级:", self.priority_spin)
        
        # 启用状态
        self.enabled_check = CheckBox("启用此路由规则")
        self.enabled_check.setChecked(True)
        basic_layout.addRow("", self.enabled_check)
        
        scroll_layout.addWidget(basic_card)
        
        # 条件配置卡片
        condition_card = CardWidget()
        condition_layout = QVBoxLayout(condition_card)
        condition_layout.setContentsMargins(20, 20, 20, 20)
        
        condition_title = SubtitleLabel("条件配置")
        condition_layout.addWidget(condition_title)
        
        self.condition_edit = TextEdit()
        self.condition_edit.setPlaceholderText("输入匹配条件（如关键词、正则表达式等）")
        self.condition_edit.setMaximumHeight(100)
        condition_layout.addWidget(self.condition_edit)
        
        # 条件说明
        condition_help = SubtitleLabel()
        condition_help.setText("""
条件说明：
• 关键词匹配：直接输入要匹配的关键词
• 正则表达式：输入正则表达式模式
• 用户权限：输入权限名称（如ADMIN、OWNER）
• 群组ID：输入群组ID号码
• 用户ID：输入用户QQ号
• 时间条件：输入时间格式（如HH:MM）
• 自定义条件：输入自定义条件函数名
        """)
        condition_help.setWordWrap(True)
        condition_layout.addWidget(condition_help)
        
        scroll_layout.addWidget(condition_card)
        
        # 描述卡片
        desc_card = CardWidget()
        desc_layout = QVBoxLayout(desc_card)
        desc_layout.setContentsMargins(20, 20, 20, 20)
        
        desc_title = SubtitleLabel("描述信息")
        desc_layout.addWidget(desc_title)
        
        self.description_edit = TextEdit()
        self.description_edit.setPlaceholderText("输入路由规则的描述信息（可选）")
        self.description_edit.setMaximumHeight(80)
        desc_layout.addWidget(self.description_edit)
        
        scroll_layout.addWidget(desc_card)
        
        scroll_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_route_data(self, route_data):
        """加载路由数据到界面"""
        self.name_edit.setText(route_data.get('name', ''))
        
        # 设置类型
        rule_type = route_data.get('rule_type', 'keyword')
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == rule_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        self.priority_spin.setValue(route_data.get('priority', 100))
        self.enabled_check.setChecked(route_data.get('enabled', True))
        self.condition_edit.setText(route_data.get('condition', ''))
        self.description_edit.setText(route_data.get('description', ''))
    
    def get_route_data(self):
        """获取路由数据"""
        return {
            'name': self.name_edit.text(),
            'rule_type': self.type_combo.currentData(),
            'priority': self.priority_spin.value(),
            'enabled': self.enabled_check.isChecked(),
            'condition': self.condition_edit.toPlainText(),
            'description': self.description_edit.toPlainText()
        }


class StepEditDialog(QDialog):
    """步骤编辑对话框"""
    
    def __init__(self, parent=None, step_data=None):
        super().__init__(parent)
        self.step_data = step_data
        self.setupUi()
        if step_data:
            self.load_step_data(step_data)
        
        # 连接类型变化事件
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        self.on_type_changed()  # 初始化配置界面
    
    def setupUi(self):
        self.setWindowTitle("编辑执行步骤")
        self.setMinimumSize(500, 500)
        self.resize(600, 600)
        
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = TitleLabel("执行步骤配置")
        layout.addWidget(title_label)
        
        # 滚动区域
        scroll_area = ScrollArea()
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        
        # 基本信息卡片
        basic_card = CardWidget()
        basic_layout = QFormLayout(basic_card)
        basic_layout.setContentsMargins(20, 20, 20, 20)
        
        # 步骤名称
        self.name_edit = LineEdit()
        self.name_edit.setPlaceholderText("输入步骤名称")
        basic_layout.addRow("名称:", self.name_edit)
        
        # 步骤类型
        self.type_combo = ComboBox()
        self.type_combo.addItem("调用插件", "plugin")
        self.type_combo.addItem("条件判断", "condition")
        self.type_combo.addItem("发送消息", "message")
        self.type_combo.addItem("设置变量", "variable")
        self.type_combo.addItem("延迟执行", "delay")
        self.type_combo.addItem("停止工作流", "stop")
        basic_layout.addRow("类型:", self.type_combo)
        
        # 启用状态
        self.enabled_check = CheckBox("启用此步骤")
        self.enabled_check.setChecked(True)
        basic_layout.addRow("", self.enabled_check)
        
        self.scroll_layout.addWidget(basic_card)
        
        # 动态配置区域（根据步骤类型变化）
        self.config_card = CardWidget()
        self.config_layout = QVBoxLayout(self.config_card)
        self.config_layout.setContentsMargins(20, 20, 20, 20)
        
        self.scroll_layout.addWidget(self.config_card)
        
        # 描述卡片
        desc_card = CardWidget()
        desc_layout = QVBoxLayout(desc_card)
        desc_layout.setContentsMargins(20, 20, 20, 20)
        
        desc_title = SubtitleLabel("描述信息")
        desc_layout.addWidget(desc_title)
        
        self.description_edit = TextEdit()
        self.description_edit.setPlaceholderText("输入步骤的描述信息（可选）")
        self.description_edit.setMaximumHeight(80)
        desc_layout.addWidget(self.description_edit)
        
        self.scroll_layout.addWidget(desc_card)
        
        self.scroll_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def clear_config_layout(self):
        """清空配置布局"""
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def on_type_changed(self):
        """步骤类型变化时更新配置界面"""
        self.clear_config_layout()
        
        step_type = self.type_combo.currentData()
        config_title = SubtitleLabel("配置参数")
        self.config_layout.addWidget(config_title)
        
        if step_type == "plugin":
            self.setup_plugin_config()
        elif step_type == "condition":
            self.setup_condition_config()
        elif step_type == "message":
            self.setup_message_config()
        elif step_type == "variable":
            self.setup_variable_config()
        elif step_type == "delay":
            self.setup_delay_config()
        elif step_type == "stop":
            self.setup_stop_config()
    
    def setup_plugin_config(self):
        """设置插件配置界面"""
        form_layout = QFormLayout()
        
        self.plugin_name_edit = LineEdit()
        self.plugin_name_edit.setPlaceholderText("输入插件名称")
        form_layout.addRow("插件名称:", self.plugin_name_edit)
        
        self.plugin_params_edit = PlainTextEdit()
        self.plugin_params_edit.setPlaceholderText('输入插件参数（JSON格式）\n例如：{"param1": "value1", "param2": "value2"}')
        self.plugin_params_edit.setMaximumHeight(100)
        form_layout.addRow("插件参数:", self.plugin_params_edit)
        
        self.save_result_check = CheckBox("保存执行结果")
        form_layout.addRow("", self.save_result_check)
        
        self.result_var_edit = LineEdit()
        self.result_var_edit.setPlaceholderText("结果变量名")
        self.result_var_edit.setEnabled(False)
        form_layout.addRow("结果变量:", self.result_var_edit)
        
        # 连接保存结果复选框事件
        self.save_result_check.toggled.connect(self.result_var_edit.setEnabled)
        
        self.config_layout.addLayout(form_layout)
    
    def setup_condition_config(self):
        """设置条件配置界面"""
        form_layout = QFormLayout()
        
        self.condition_edit = TextEdit()
        self.condition_edit.setPlaceholderText("输入条件表达式\n例如：${user_id} == '123456' or 'ADMIN' in ${user_permissions}")
        self.condition_edit.setMaximumHeight(80)
        form_layout.addRow("条件表达式:", self.condition_edit)
        
        self.true_steps_edit = LineEdit()
        self.true_steps_edit.setPlaceholderText("条件为真时跳转的步骤ID（可选）")
        form_layout.addRow("真分支步骤:", self.true_steps_edit)
        
        self.false_steps_edit = LineEdit()
        self.false_steps_edit.setPlaceholderText("条件为假时跳转的步骤ID（可选）")
        form_layout.addRow("假分支步骤:", self.false_steps_edit)
        
        self.config_layout.addLayout(form_layout)
        
        # 添加说明
        help_text = SubtitleLabel("""
条件表达式说明：
• 使用 ${变量名} 引用工作流变量或消息上下文
• 支持Python表达式：==, !=, <, >, <=, >=, and, or, not, in
• 例如：${message} == 'hello' 或 'ADMIN' in ${user_permissions}
        """)
        help_text.setWordWrap(True)
        self.config_layout.addWidget(help_text)
    
    def setup_message_config(self):
        """设置消息配置界面"""
        form_layout = QFormLayout()
        
        self.message_edit = TextEdit()
        self.message_edit.setPlaceholderText("输入要发送的消息内容\n可以使用 ${变量名} 引用变量")
        self.message_edit.setMaximumHeight(100)
        form_layout.addRow("消息内容:", self.message_edit)
        
        self.reply_check = CheckBox("作为回复消息发送")
        form_layout.addRow("", self.reply_check)
        
        self.config_layout.addLayout(form_layout)
    
    def setup_variable_config(self):
        """设置变量配置界面"""
        form_layout = QFormLayout()
        
        self.var_name_edit = LineEdit()
        self.var_name_edit.setPlaceholderText("输入变量名")
        form_layout.addRow("变量名:", self.var_name_edit)
        
        self.var_value_edit = TextEdit()
        self.var_value_edit.setPlaceholderText("输入变量值\n可以使用 ${变量名} 引用其他变量")
        self.var_value_edit.setMaximumHeight(80)
        form_layout.addRow("变量值:", self.var_value_edit)
        
        self.config_layout.addLayout(form_layout)
    
    def setup_delay_config(self):
        """设置延迟配置界面"""
        form_layout = QFormLayout()
        
        self.delay_spin = SpinBox()
        self.delay_spin.setRange(1, 3600)
        self.delay_spin.setValue(1)
        self.delay_spin.setSuffix(" 秒")
        form_layout.addRow("延迟时间:", self.delay_spin)
        
        self.config_layout.addLayout(form_layout)
    
    def setup_stop_config(self):
        """设置停止配置界面"""
        help_text = SubtitleLabel("此步骤将停止工作流的执行，无需额外配置。")
        self.config_layout.addWidget(help_text)
    
    def load_step_data(self, step_data):
        """加载步骤数据到界面"""
        self.name_edit.setText(step_data.get('name', ''))
        
        # 设置类型
        step_type = step_data.get('type', 'plugin')
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == step_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        self.enabled_check.setChecked(step_data.get('enabled', True))
        self.description_edit.setText(step_data.get('description', ''))
        
        # 加载配置数据
        config = step_data.get('config', {})
        self.load_config_data(step_type, config)
    
    def load_config_data(self, step_type, config):
        """根据步骤类型加载配置数据"""
        if step_type == "plugin":
            if hasattr(self, 'plugin_name_edit'):
                self.plugin_name_edit.setText(config.get('plugin_name', ''))
                self.plugin_params_edit.setPlainText(str(config.get('parameters', {})))
                self.save_result_check.setChecked(config.get('save_result', False))
                self.result_var_edit.setText(config.get('result_variable', ''))
        elif step_type == "condition":
            if hasattr(self, 'condition_edit'):
                self.condition_edit.setText(config.get('condition', ''))
                self.true_steps_edit.setText(','.join(config.get('true_steps', [])))
                self.false_steps_edit.setText(','.join(config.get('false_steps', [])))
        elif step_type == "message":
            if hasattr(self, 'message_edit'):
                self.message_edit.setText(config.get('message', ''))
                self.reply_check.setChecked(config.get('reply', False))
        elif step_type == "variable":
            if hasattr(self, 'var_name_edit'):
                self.var_name_edit.setText(config.get('variable_name', ''))
                self.var_value_edit.setText(config.get('variable_value', ''))
        elif step_type == "delay":
            if hasattr(self, 'delay_spin'):
                self.delay_spin.setValue(config.get('delay', 1))
    
    def get_step_data(self):
        """获取步骤数据"""
        step_type = self.type_combo.currentData()
        config = self.get_config_data(step_type)
        
        return {
            'name': self.name_edit.text(),
            'type': step_type,
            'enabled': self.enabled_check.isChecked(),
            'description': self.description_edit.toPlainText(),
            'config': config
        }
    
    def get_config_data(self, step_type):
        """根据步骤类型获取配置数据"""
        config = {}
        
        if step_type == "plugin":
            config['plugin_name'] = self.plugin_name_edit.text()
            try:
                import json
                params_text = self.plugin_params_edit.toPlainText().strip()
                if params_text:
                    config['parameters'] = json.loads(params_text)
                else:
                    config['parameters'] = {}
            except json.JSONDecodeError:
                config['parameters'] = {}
            config['save_result'] = self.save_result_check.isChecked()
            config['result_variable'] = self.result_var_edit.text()
        elif step_type == "condition":
            config['condition'] = self.condition_edit.toPlainText()
            true_steps = [s.strip() for s in self.true_steps_edit.text().split(',') if s.strip()]
            false_steps = [s.strip() for s in self.false_steps_edit.text().split(',') if s.strip()]
            config['true_steps'] = true_steps
            config['false_steps'] = false_steps
        elif step_type == "message":
            config['message'] = self.message_edit.toPlainText()
            config['reply'] = self.reply_check.isChecked()
        elif step_type == "variable":
            config['variable_name'] = self.var_name_edit.text()
            config['variable_value'] = self.var_value_edit.toPlainText()
        elif step_type == "delay":
            config['delay'] = self.delay_spin.value()
        
        return config