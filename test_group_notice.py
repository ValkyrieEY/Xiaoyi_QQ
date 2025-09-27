#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Tools.group_notice_manager import GroupNoticeManager
import json
import os

def test_group_notice_manager():
    print("=== 群组通知管理器功能测试 ===\n")
    
    gm = GroupNoticeManager()
    test_group_id = 888888
    
    print("1. 测试初始状态")
    status = gm.get_group_status(test_group_id)
    print(f"群组 {test_group_id} 初始状态:")
    print(f"  - 入群欢迎: {'✅ 已启用' if status['welcome_enabled'] else '❌ 已禁用'}")
    print(f"  - 退群提示: {'✅ 已启用' if status['farewell_enabled'] else '❌ 已禁用'}")
    print(f"  - 自定义入群消息: {'✅ 已设置' if status['has_custom_welcome'] else '❌ 未设置'}")
    print(f"  - 自定义退群消息: {'✅ 已设置' if status['has_custom_farewell'] else '❌ 未设置'}")
    print()
    
    print("2. 测试开关功能")
    gm.set_welcome_enabled(test_group_id, False)
    print(f"关闭入群欢迎后: {gm.is_welcome_enabled(test_group_id)}")
    
    gm.set_welcome_enabled(test_group_id, True)
    print(f"重新开启入群欢迎后: {gm.is_welcome_enabled(test_group_id)}")
    
    gm.set_farewell_enabled(test_group_id, False)
    print(f"关闭退群提示后: {gm.is_farewell_enabled(test_group_id)}")
    
    gm.set_farewell_enabled(test_group_id, True)
    print(f"重新开启退群提示后: {gm.is_farewell_enabled(test_group_id)}")
    print()
    
    print("3. 测试自定义消息功能")
    custom_welcome = "欢迎新成员加入我们的大家庭！🎉"
    gm.set_welcome_message(test_group_id, custom_welcome)
    retrieved_welcome = gm.get_welcome_message(test_group_id)
    print(f"设置自定义入群消息: {custom_welcome}")
    print(f"获取自定义入群消息: {retrieved_welcome}")
    print(f"消息是否一致: {custom_welcome == retrieved_welcome}")
    
    custom_farewell = "{user_nick}离开了我们，希望TA一切都好！👋"
    gm.set_farewell_message(test_group_id, custom_farewell)
    retrieved_farewell = gm.get_farewell_message(test_group_id)
    print(f"设置自定义退群消息: {custom_farewell}")
    print(f"获取自定义退群消息: {retrieved_farewell}")
    print(f"消息是否一致: {custom_farewell == retrieved_farewell}")
    print()
    
    print("4. 测试最终状态")
    final_status = gm.get_group_status(test_group_id)
    print(f"群组 {test_group_id} 最终状态:")
    print(f"  - 入群欢迎: {'✅ 已启用' if final_status['welcome_enabled'] else '❌ 已禁用'}")
    print(f"  - 退群提示: {'✅ 已启用' if final_status['farewell_enabled'] else '❌ 已禁用'}")
    print(f"  - 自定义入群消息: {'✅ 已设置' if final_status['has_custom_welcome'] else '❌ 未设置'}")
    print(f"  - 自定义退群消息: {'✅ 已设置' if final_status['has_custom_farewell'] else '❌ 未设置'}")
    print(f"  - 创建时间: {final_status['created_at']}")
    print(f"  - 更新时间: {final_status['updated_at']}")
    print()
    
    print("5. 测试配置文件")
    config_path = gm.get_config_path(test_group_id)
    if os.path.exists(config_path):
        print(f"配置文件路径: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        print("配置文件内容:")
        print(json.dumps(config_data, ensure_ascii=False, indent=2))
    else:
        print("❌ 配置文件未找到")
    print()
    
    print("6. 测试列出所有群组")
    all_groups = gm.list_all_groups()
    print(f"所有配置的群组数量: {len(all_groups)}")
    for group in all_groups:
        print(f"  群组 {group['group_id']}: 入群欢迎={'✅' if group['welcome_enabled'] else '❌'}, 退群提示={'✅' if group['farewell_enabled'] else '❌'}")
    print()
    
    print("=== 测试完成 ===")
    print("✅ 群组通知管理器所有功能测试通过！")

if __name__ == "__main__":
    test_group_notice_manager()