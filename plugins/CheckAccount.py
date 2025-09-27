import re
import json
from datetime import datetime

from Hyper import Configurator
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

TRIGGHT_KEYWORD = "开"
HELP_MESSAGE = f"{Configurator.cm.get_cfg().others["reminder"]}开 【@一个用户/QQ号】 —> 打开该用户的账户 👁"

async def on_message(event, actions, Manager, Segments, order, bot_name, bot_name_en, ONE_SLOGAN):
    uid = 0
    for i in event.message:
        if isinstance(i, Segments.At):
            uid = int(i.qq)
            break
        
    if uid == 0:
        uid = order[order.find(f"{TRIGGHT_KEYWORD} ") + len(f"{TRIGGHT_KEYWORD} "):].strip()
        
    print(f"try to get_user {uid}")
    nikename = (await actions.get_stranger_info(uid)).data.raw
    print(f"获取 {nikename} 成功")
    if len(nikename) == 0:
        r = f'''{bot_name} {bot_name_en} - {ONE_SLOGAN}
————————————————————
失败: {uid} 不是一个有效的用户'''

        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(r)))
        
    else:
        avatar, r = parse_user_info(nikename)
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Image(avatar), Segments.Text(r)))
        
    return True

def parse_user_info(user_dict):
    try:
        avatar = user_dict.get('avatar', '')
        register_time = user_dict.get('RegisterTime', '')
        try:
            dt = datetime.strptime(register_time, '%Y-%m-%dT%H:%M:%SZ')
            register_time = dt.strftime('%Y.%m.%d %H:%M:%S')
        except (ValueError, TypeError):
            register_time = '未知时间'
            
        business = user_dict.get('Business', [])
        is_vip = any(item.get('type') == 1 for item in business)
        vip_level = next((item.get('level', 0) for item in business if item.get('type') == 1), 0)
        is_year_vip = any(item.get('isyear') == 1 for item in business if item.get('type') == 1)

        status_msg = user_dict.get('status', {}).get('message', '暂无状态')

        result = f"""昵称: {user_dict.get('nickname', '未知')}
状态: {status_msg}
QQ号: {user_dict.get('user_id', '未知')}
QID: {user_dict.get('q_id', '未知')}
性别: {'男' if user_dict.get('sex') == 'male' else '女'}
年龄: {user_dict.get('age', '未知')}
QQ等级: {user_dict.get('level', '未知')}
个性签名: {user_dict.get('sign', '暂无签名')}
注册时间: {register_time}
超级会员: {'是' if is_vip else '否'}
会员等级: {vip_level}
年费会员: {'是' if is_year_vip else '否'}"""

        return (avatar, result)

    except Exception as e:
        print(f"解析失败: {e}")
        return ("", "无法打开该用户的账户")