# -*- coding: utf-8 -*-

"""
工作流管理器
负责工作流的配置、路由、执行等功能
"""

import json
import os
import re
import uuid
import asyncio
import importlib.util
import sys
import traceback
from typing import Dict, List, Any, Optional, Union, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime


class StepType(Enum):
    """步骤类型枚举"""
    PLUGIN = "plugin"           # 调用插件
    CONDITION = "condition"     # 条件判断
    MESSAGE = "message"         # 发送消息
    VARIABLE = "variable"       # 设置变量
    DELAY = "delay"            # 延迟执行
    STOP = "stop"              # 停止工作流


class RoutingRule(Enum):
    """路由规则类型"""
    KEYWORD = "keyword"         # 关键词匹配
    REGEX = "regex"            # 正则表达式
    USER_PERMISSION = "user_permission"  # 用户权限
    GROUP_ID = "group_id"      # 群组ID
    USER_ID = "user_id"        # 用户ID
    TIME = "time"              # 时间条件
    CUSTOM = "custom"          # 自定义条件


@dataclass
class WorkflowStep:
    """工作流步骤"""
    id: str
    name: str
    type: StepType
    config: Dict[str, Any]
    enabled: bool = True
    description: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowStep':
        return cls(
            id=data['id'],
            name=data['name'],
            type=StepType(data['type']),
            config=data['config'],
            enabled=data.get('enabled', True),
            description=data.get('description', '')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'config': self.config,
            'enabled': self.enabled,
            'description': self.description
        }


@dataclass
class WorkflowRoute:
    """工作流路由规则"""
    id: str
    name: str
    rule_type: RoutingRule
    condition: str
    priority: int = 0
    enabled: bool = True
    description: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowRoute':
        return cls(
            id=data['id'],
            name=data['name'],
            rule_type=RoutingRule(data['rule_type']),
            condition=data['condition'],
            priority=data.get('priority', 0),
            enabled=data.get('enabled', True),
            description=data.get('description', '')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'rule_type': self.rule_type.value,
            'condition': self.condition,
            'priority': self.priority,
            'enabled': self.enabled,
            'description': self.description
        }


@dataclass
class Workflow:
    """工作流定义"""
    id: str
    name: str
    description: str
    routes: List[WorkflowRoute]
    steps: List[WorkflowStep]
    enabled: bool = True
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workflow':
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            routes=[WorkflowRoute.from_dict(r) for r in data['routes']],
            steps=[WorkflowStep.from_dict(s) for s in data['steps']],
            enabled=data.get('enabled', True),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', '')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'routes': [r.to_dict() for r in self.routes],
            'steps': [s.to_dict() for s in self.steps],
            'enabled': self.enabled,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class WorkflowContext:
    """工作流执行上下文"""
    def __init__(self, workflow_id: str, message_context: Dict[str, Any]):
        self.workflow_id = workflow_id
        self.message_context = message_context
        self.variables: Dict[str, Any] = {}
        self.current_step = 0
        self.execution_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.logs: List[str] = []
        self.stopped = False
    
    def log(self, message: str):
        """添加执行日志"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(f"Workflow[{self.workflow_id}]: {log_entry}")
    
    def set_variable(self, name: str, value: Any):
        """设置变量"""
        self.variables[name] = value
        self.log(f"Variable set: {name} = {value}")
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """获取变量"""
        return self.variables.get(name, default)


class WorkflowManager:
    """工作流管理器"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.workflows_dir = os.path.join(config_dir, "workflows")
        self.config_file = os.path.join(config_dir, "workflow_config.json")
        
        # 确保目录存在
        os.makedirs(self.workflows_dir, exist_ok=True)
        
        self.workflows: Dict[str, Workflow] = {}
        self.global_config: Dict[str, Any] = {}
        self.custom_conditions: Dict[str, Callable] = {}
        
        self.load_config()
        self.load_workflows()
    
    def load_config(self):
        """加载全局配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.global_config = json.load(f)
            except Exception as e:
                print(f"加载工作流配置失败: {e}")
                self.global_config = {}
        
            # 初始化默认配置
        if not self.global_config:
            self.global_config = {
                "enabled": True,
                "max_execution_time": 60,  # 最大执行时间(秒)
                "log_level": "info",
                "default_priority": 100,
                "concurrent_workflows": 10,  # 并发执行的工作流数量
                "auto_reload": True,  # 自动重载
                "debug_mode": False  # 调试模式
            }
            self.save_config()
    
    def save_config(self):
        """保存全局配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.global_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存工作流配置失败: {e}")
    
    def load_workflows(self):
        """加载所有工作流"""
        self.workflows.clear()
        
        if not os.path.exists(self.workflows_dir):
            return
        
        for filename in os.listdir(self.workflows_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.workflows_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    workflow = Workflow.from_dict(data)
                    self.workflows[workflow.id] = workflow
                    print(f"已加载工作流: {workflow.name} ({workflow.id})")
                
                except Exception as e:
                    print(f"加载工作流 {filename} 失败: {e}")
    
    def save_workflow(self, workflow: Workflow):
        """保存工作流到文件"""
        workflow.updated_at = datetime.now().isoformat()
        filepath = os.path.join(self.workflows_dir, f"{workflow.id}.json")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(workflow.to_dict(), f, ensure_ascii=False, indent=2)
            
            self.workflows[workflow.id] = workflow
            print(f"已保存工作流: {workflow.name}")
            
        except Exception as e:
            print(f"保存工作流失败: {e}")
            raise
    
    def create_workflow(self, name: str, description: str = "") -> Workflow:
        """创建新工作流"""
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            routes=[],
            steps=[]
        )
        
        self.save_workflow(workflow)
        return workflow
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """删除工作流"""
        if workflow_id not in self.workflows:
            return False
        
        filepath = os.path.join(self.workflows_dir, f"{workflow_id}.json")
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            
            del self.workflows[workflow_id]
            print(f"已删除工作流: {workflow_id}")
            return True
            
        except Exception as e:
            print(f"删除工作流失败: {e}")
            return False
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """获取工作流"""
        return self.workflows.get(workflow_id)
    
    def list_workflows(self) -> List[Workflow]:
        """列出所有工作流"""
        return list(self.workflows.values())
    
    def add_route_to_workflow(self, workflow_id: str, route: WorkflowRoute):
        """添加路由规则到工作流"""
        workflow = self.get_workflow(workflow_id)
        if workflow:
            workflow.routes.append(route)
            self.save_workflow(workflow)
    
    def add_step_to_workflow(self, workflow_id: str, step: WorkflowStep):
        """添加步骤到工作流"""
        workflow = self.get_workflow(workflow_id)
        if workflow:
            workflow.steps.append(step)
            self.save_workflow(workflow)
    
    def register_custom_condition(self, name: str, condition_func: Callable):
        """注册自定义条件函数"""
        self.custom_conditions[name] = condition_func
    
    async def route_message(self, message_context: Dict[str, Any]) -> List[str]:
        """路由消息到匹配的工作流"""
        matched_workflows = []
        
        if not self.global_config.get("enabled", True):
            return matched_workflows
        
        # 按优先级排序的所有路由规则
        all_routes = []
        for workflow in self.workflows.values():
            if workflow.enabled:
                for route in workflow.routes:
                    if route.enabled:
                        all_routes.append((workflow.id, route))
        
        # 按优先级排序
        all_routes.sort(key=lambda x: x[1].priority, reverse=True)
        
        for workflow_id, route in all_routes:
            if await self._check_route_condition(route, message_context):
                matched_workflows.append(workflow_id)
        
        return matched_workflows
    
    async def _check_route_condition(self, route: WorkflowRoute, context: Dict[str, Any]) -> bool:
        """检查路由条件是否匹配"""
        try:
            if route.rule_type == RoutingRule.KEYWORD:
                message = str(context.get('message', ''))
                return route.condition in message
            
            elif route.rule_type == RoutingRule.REGEX:
                message = str(context.get('message', ''))
                return bool(re.search(route.condition, message))
            
            elif route.rule_type == RoutingRule.USER_PERMISSION:
                user_permissions = context.get('user_permissions', [])
                return route.condition in user_permissions
            
            elif route.rule_type == RoutingRule.GROUP_ID:
                group_id = str(context.get('group_id', ''))
                return group_id == route.condition
            
            elif route.rule_type == RoutingRule.USER_ID:
                user_id = str(context.get('user_id', ''))
                return user_id == route.condition
            
            elif route.rule_type == RoutingRule.TIME:
                current_time = datetime.now().strftime("%H:%M")
                return current_time == route.condition
            
            elif route.rule_type == RoutingRule.CUSTOM:
                if route.condition in self.custom_conditions:
                    return await self.custom_conditions[route.condition](context)
            
            return False
            
        except Exception as e:
            print(f"检查路由条件失败: {e}")
            return False


class WorkflowExecutor:
    """工作流执行器"""
    
    def __init__(self, workflow_manager: WorkflowManager, plugins: List[Any]):
        self.workflow_manager = workflow_manager
        self.plugins = plugins
        self.active_executions: Dict[str, WorkflowContext] = {}
    
    async def execute_workflow(self, workflow_id: str, message_context: Dict[str, Any]) -> bool:
        """执行工作流"""
        workflow = self.workflow_manager.get_workflow(workflow_id)
        if not workflow or not workflow.enabled:
            return False
        
        context = WorkflowContext(workflow_id, message_context)
        self.active_executions[context.execution_id] = context
        
        context.log(f"开始执行工作流: {workflow.name}")
        
        try:
            # 改为基于步骤ID的执行模式，支持条件分支
            current_step_index = 0
            executed_steps = set()  # 防止无限循环
            
            while current_step_index < len(workflow.steps):
                if context.stopped:
                    break
                
                step = workflow.steps[current_step_index]
                
                if not step.enabled or step.id in executed_steps:
                    current_step_index += 1
                    continue
                
                executed_steps.add(step.id)
                context.current_step = current_step_index
                context.log(f"执行步骤 {current_step_index+1}: {step.name}")
                
                # 执行步骤并获取下一步操作
                next_action = await self._execute_step_with_branching(step, context, workflow)
                
                if next_action == "stop":
                    break
                elif next_action == "continue":
                    current_step_index += 1
                elif isinstance(next_action, str) and next_action.startswith("jump:"):
                    # 跳转到指定步骤
                    target_step_id = next_action[5:]  # 去除 "jump:" 前缀
                    target_index = self._find_step_index(workflow, target_step_id)
                    if target_index >= 0:
                        current_step_index = target_index
                        context.log(f"跳转到步骤: {target_step_id}")
                    else:
                        context.log(f"找不到目标步骤: {target_step_id}")
                        current_step_index += 1
                else:
                    # 默认继续下一步
                    current_step_index += 1
            
            context.log("工作流执行完成")
            return True
            
        except Exception as e:
            context.log(f"工作流执行异常: {e}")
            traceback.print_exc()
            return False
        
        finally:
            if context.execution_id in self.active_executions:
                del self.active_executions[context.execution_id]
    
    def _find_step_index(self, workflow: 'Workflow', step_id: str) -> int:
        """查找步骤ID对应的索引"""
        for i, step in enumerate(workflow.steps):
            if step.id == step_id:
                return i
        return -1
    
    async def _execute_step_with_branching(self, step: WorkflowStep, context: WorkflowContext, workflow: 'Workflow') -> str:
        """执行单个步骤并返回下一步操作"""
        try:
            if step.type == StepType.PLUGIN:
                success = await self._execute_plugin_step(step, context)
                return "continue" if success else "stop"
            elif step.type == StepType.CONDITION:
                result = await self._execute_condition_step(step, context)
                # 根据条件结果决定下一步
                if result and step.config.get('true_steps'):
                    # 条件为真，跳转到真分支
                    true_steps = step.config['true_steps']
                    if true_steps:
                        return f"jump:{true_steps[0]}"
                elif not result and step.config.get('false_steps'):
                    # 条件为假，跳转到假分支
                    false_steps = step.config['false_steps']
                    if false_steps:
                        return f"jump:{false_steps[0]}"
                return "continue"
            elif step.type == StepType.MESSAGE:
                success = await self._execute_message_step(step, context)
                return "continue" if success else "stop"
            elif step.type == StepType.VARIABLE:
                success = await self._execute_variable_step(step, context)
                return "continue" if success else "stop"
            elif step.type == StepType.DELAY:
                success = await self._execute_delay_step(step, context)
                return "continue" if success else "stop"
            elif step.type == StepType.STOP:
                context.stopped = True
                context.log("工作流被停止")
                return "stop"
            
            return "continue"
            
        except Exception as e:
            context.log(f"步骤执行异常: {e}")
            return "stop"
    
    async def _execute_plugin_step(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """执行插件步骤"""
        plugin_name = step.config.get('plugin_name')
        if not plugin_name:
            context.log("插件名称未指定")
            return False
        
        # 查找插件
        target_plugin = None
        for plugin in self.plugins:
            if hasattr(plugin, '__name__') and plugin_name in plugin.__name__:
                target_plugin = plugin
                break
            elif hasattr(plugin, 'TRIGGHT_KEYWORD') and plugin.TRIGGHT_KEYWORD == plugin_name:
                target_plugin = plugin
                break
        
        if not target_plugin:
            context.log(f"插件未找到: {plugin_name}")
            return False
        
        try:
            # 调用插件
            if hasattr(target_plugin, 'on_message'):
                # 动态获取插件函数的参数签名
                import inspect
                on_message_params = inspect.signature(target_plugin.on_message).parameters
                
                # 准备插件参数 - 只传递插件实际需要的参数
                plugin_kwargs = {}
                available_context = context.message_context.copy()
                available_context.update(step.config.get('parameters', {}))
                
                for param_name, param in on_message_params.items():
                    if param_name in available_context:
                        plugin_kwargs[param_name] = available_context[param_name]
                    elif param.default is not inspect.Parameter.empty:
                        # 使用默认值，不需要显式传递
                        pass
                    else:
                        context.log(f"插件 {target_plugin.__name__} 缺少必需参数: {param_name}")
                        return False
                
                result = await target_plugin.on_message(**plugin_kwargs)
                context.log(f"插件执行结果: {result}")
                
                # 保存结果到变量
                if step.config.get('save_result'):
                    var_name = step.config.get('result_variable', f'step_{step.id}_result')
                    context.set_variable(var_name, result)
                
                return True
            else:
                context.log("插件没有 on_message 方法")
                return False
                
        except Exception as e:
            context.log(f"插件执行异常: {e}")
            return False
    
    async def _execute_condition_step(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """执行条件步骤"""
        condition = step.config.get('condition')
        if not condition:
            return False
        
        # 简单的条件判断实现
        try:
            # 合并所有可用的变量（工作流变量 + 消息上下文）
            all_variables = {}
            all_variables.update(context.message_context)  # 消息上下文
            all_variables.update(context.variables)       # 工作流变量
            
            # 替换条件中的变量
            processed_condition = condition
            for var_name, var_value in all_variables.items():
                placeholder = f"${{{var_name}}}"
                if placeholder in processed_condition:
                    # 处理特殊类型的变量
                    if isinstance(var_value, list):
                        # 列表类型，用于repr表示
                        processed_condition = processed_condition.replace(placeholder, repr(var_value))
                    else:
                        # 普通变量，转为字符串后用repr表示以保持引号
                        processed_condition = processed_condition.replace(placeholder, repr(str(var_value)))
            
            # 评估条件，传入所有可用变量作为上下文
            safe_globals = {"__builtins__": {}}
            result = eval(processed_condition, safe_globals, all_variables)
            context.log(f"条件判断: {processed_condition} = {result}")
            
            return bool(result)
            
        except Exception as e:
            context.log(f"条件判断异常: {e}")
            return False
    
    async def _execute_message_step(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """执行消息步骤"""
        message = step.config.get('message', '')
        if not message:
            return False
        
        # 合并所有可用的变量（工作流变量 + 消息上下文）
        all_variables = {}
        all_variables.update(context.message_context)  # 消息上下文
        all_variables.update(context.variables)       # 工作流变量
        
        # 替换变量
        for var_name, var_value in all_variables.items():
            message = message.replace(f"${{{var_name}}}", str(var_value))
        
        # 从消息上下文中获取actions和相关信息
        actions = context.message_context.get('actions')
        group_id = context.message_context.get('group_id')
        user_id = context.message_context.get('user_id')
        message_id = context.message_context.get('message_id')
        
        if actions:
            try:
                # 导入所需的类（需要从主程序上下文获取）
                from Hyper import Manager, Segments
                
                if group_id:
                    # 群聊消息
                    if message_id and step.config.get('reply', False):
                        # 回复消息
                        await actions.send(
                            group_id=group_id,
                            message=Manager.Message(Segments.Reply(message_id), Segments.Text(message))
                        )
                    else:
                        # 普通消息
                        await actions.send(
                            group_id=group_id,
                            message=Manager.Message(Segments.Text(message))
                        )
                elif user_id:
                    # 私聊消息
                    await actions.send(
                        user_id=user_id,
                        message=Manager.Message(Segments.Text(message))
                    )
                
                context.log(f"消息已发送: {message}")
                return True
                
            except Exception as e:
                context.log(f"发送消息失败: {e}")
                return False
        else:
            # 没有actions，只记录日志
            context.log(f"模拟发送消息: {message}")
            context.set_variable('last_message', message)
            return True
    
    async def _execute_variable_step(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """执行变量步骤"""
        var_name = step.config.get('variable_name')
        var_value = step.config.get('variable_value')
        
        if not var_name:
            return False
        
        # 合并所有可用的变量（工作流变量 + 消息上下文）
        all_variables = {}
        all_variables.update(context.message_context)  # 消息上下文
        all_variables.update(context.variables)       # 工作流变量
        
        # 替换变量值中的其他变量
        if isinstance(var_value, str):
            for name, value in all_variables.items():
                var_value = var_value.replace(f"${{{name}}}", str(value))
        
        context.set_variable(var_name, var_value)
        return True
    
    async def _execute_delay_step(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """执行延迟步骤"""
        delay_seconds = step.config.get('delay', 1)
        context.log(f"延迟 {delay_seconds} 秒")
        await asyncio.sleep(delay_seconds)
        return True