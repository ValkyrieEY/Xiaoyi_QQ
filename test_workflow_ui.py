#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试工作流UI的简单脚本
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_workflow_imports():
    """测试工作流相关的导入"""
    try:
        print("测试工作流管理器导入...")
        from Tools.workflow_manager import WorkflowManager, Workflow, WorkflowRoute, WorkflowStep, StepType, RoutingRule
        print("✓ 工作流管理器导入成功")
        
        print("测试工作流UI导入...")
        from wizardWindows.Ui_JianerSetupWorkflow import Ui_Form
        print("✓ 工作流UI导入成功")
        
        print("测试工作流对话框导入...")
        from wizardWindows.Ui_JianerSetupWorkflowDialogs import RouteEditDialog, StepEditDialog
        print("✓ 工作流对话框导入成功")
        
        print("测试WizardUIs导入...")
        from WizardUIs import JianerSetupWorkflow
        print("✓ WizardUIs导入成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_manager():
    """测试工作流管理器基本功能"""
    try:
        print("\n测试工作流管理器功能...")
        from Tools.workflow_manager import WorkflowManager
        
        # 创建工作流管理器
        wm = WorkflowManager()
        print("✓ 工作流管理器创建成功")
        
        # 列出工作流
        workflows = wm.list_workflows()
        print(f"✓ 发现 {len(workflows)} 个工作流")
        
        for workflow in workflows:
            print(f"  - {workflow.name} ({workflow.id}) - {'启用' if workflow.enabled else '禁用'}")
            print(f"    路由规则: {len(workflow.routes)} 个")
            print(f"    执行步骤: {len(workflow.steps)} 个")
        
        return True
        
    except Exception as e:
        print(f"✗ 工作流管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_creation():
    """测试UI创建"""
    try:
        print("\n测试UI创建...")
        
        from PySide6.QtWidgets import QApplication
        from WizardUIs import JianerSetupWorkflow
        from Tools.workflow_manager import WorkflowManager
        
        # 创建应用程序
        app = QApplication(sys.argv)
        
        # 创建工作流UI
        workflow_ui = JianerSetupWorkflow()
        print("✓ 工作流UI创建成功")
        
        # 创建工作流管理器并连接
        wm = WorkflowManager()
        workflow_ui.set_workflow_manager(wm)
        print("✓ 工作流管理器连接成功")
        
        # 不显示UI，只测试创建
        print("✓ UI测试完成")
        
        return True
        
    except Exception as e:
        print(f"✗ UI创建测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始测试工作流UI系统...")
    print("=" * 50)
    
    # 测试导入
    if not test_workflow_imports():
        return False
    
    # 测试工作流管理器
    if not test_workflow_manager():
        return False
    
    # 测试UI创建
    if not test_ui_creation():
        return False
    
    print("\n" + "=" * 50)
    print("✓ 所有测试通过！工作流UI系统已就绪。")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)