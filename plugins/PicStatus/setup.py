import os
from Hyper import Configurator as _C
from .utils import InfoCollector
from .templates import template
from .config import config

TRIGGHT_KEYWORD = "Any"

async def _perm(e):
    u = str(e.user_id)
    try:
        return (
            u in _C.cm.get_cfg().others["ROOT_User"]
            or u in open("./Super_User.ini", "r").read().splitlines()
            or u in open("./Manage_User.ini", "r").read().splitlines()
        )
    except Exception:
        return False

async def on_message(event, actions, Manager, Segments):
    if not hasattr(event, "message"):
        return False
    
    m = str(event.message).strip()
    r = _C.cm.get_cfg().others.get('reminder', '')
    
    # 检查命令
    if not any(m == f"{r}{cmd}" for cmd in config.COMMAND):
        return False
    
    # 检查权限
    if config.ONLY_SUPERUSER and not await _perm(event):
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("你没有权限执行此操作"))
        )
        return True
    
    # 检查是否需要@机器人
    if config.NEED_AT and not event.is_tome():
        return False
    
    try:
        # 收集系统信息
        info = await InfoCollector.collect_all()
        
        # 渲染状态图片
        img_data = template.render(info)
        
        # 发送图片
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message([Segments.Image(img_data)])
        )
    except Exception as e:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(f"获取系统状态失败: {e}"))
        )
    
    return True

print("[Xiaoyi_QQ]系统状态监控插件已加载") 