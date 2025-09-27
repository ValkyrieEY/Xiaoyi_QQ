#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from ai_plugins.memory_manager import AIMemoryManager, MemoryMode

def test_memory_system():
    print("=== AI记忆系统测试 ===")
    
    memory_manager = AIMemoryManager()
    
    # 测试用户和群组ID
    user1_id = "test_user_1"
    user2_id = "test_user_2"
    group_id = "test_group"
    
    print("\n1. 测试默认记忆模式（应该是GLOBAL）")
    mode1 = memory_manager.get_user_memory_mode(user1_id)
    print(f"用户1默认记忆模式: {mode1.value}")
    
    print("\n2. 测试设置个人记忆模式")
    memory_manager.set_user_memory_mode(user1_id, MemoryMode.PERSONAL)
    mode1_new = memory_manager.get_user_memory_mode(user1_id)
    print(f"用户1新记忆模式: {mode1_new.value}")
    
    print("\n3. 测试全局记忆模式下的上下文ID")
    memory_manager.set_user_memory_mode(user1_id, MemoryMode.GLOBAL)
    memory_manager.set_user_memory_mode(user2_id, MemoryMode.GLOBAL)
    
    context_id_1 = memory_manager.get_context_id(user1_id, group_id)
    context_id_2 = memory_manager.get_context_id(user2_id, group_id)
    print(f"用户1全局模式上下文ID: {context_id_1}")
    print(f"用户2全局模式上下文ID: {context_id_2}")
    print(f"两个用户在全局模式下是否共享上下文: {context_id_1 == context_id_2}")
    
    print("\n4. 测试个人记忆模式下的上下文ID")
    memory_manager.set_user_memory_mode(user1_id, MemoryMode.PERSONAL)
    memory_manager.set_user_memory_mode(user2_id, MemoryMode.PERSONAL)
    
    context_id_1_personal = memory_manager.get_context_id(user1_id, group_id)
    context_id_2_personal = memory_manager.get_context_id(user2_id, group_id)
    print(f"用户1个人模式上下文ID: {context_id_1_personal}")
    print(f"用户2个人模式上下文ID: {context_id_2_personal}")
    print(f"两个用户在个人模式下是否独立上下文: {context_id_1_personal != context_id_2_personal}")
    
    print("\n5. 测试添加消息到记忆")
    memory_manager.set_user_memory_mode(user1_id, MemoryMode.GLOBAL)
    memory_manager.set_user_memory_mode(user2_id, MemoryMode.GLOBAL)
    
    memory_manager.add_message(user1_id, group_id, "测试用户1", "你好，我是用户1", "user")
    memory_manager.add_message(user2_id, group_id, "测试用户2", "你好，我是用户2", "user")
    memory_manager.add_message(user1_id, group_id, "简儿", "你们好！很高兴认识你们。", "assistant")
    
    print("已添加测试消息到全局记忆")
    
    print("\n6. 测试获取AI上下文")
    ai_context = memory_manager.get_context_for_ai(user1_id, group_id, "你是一个可爱的AI助手", "简儿")
    print("AI上下文格式:")
    for i, msg in enumerate(ai_context):
        print(f"  {i+1}. {msg['role']}: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}")
    
    print("\n7. 测试记忆状态")
    status = memory_manager.get_memory_status(user1_id, group_id)
    print(f"记忆状态: {status}")
    
    print("\n8. 测试全局预设")
    preset_name = "测试预设"
    memory_manager.set_global_preset(group_id, preset_name)
    saved_preset = memory_manager.get_global_preset(group_id)
    print(f"设置的全局预设: {preset_name}")
    print(f"获取的全局预设: {saved_preset}")
    print(f"全局预设设置成功: {preset_name == saved_preset}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_memory_system()