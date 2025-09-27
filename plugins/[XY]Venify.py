import os
import json
import random
import asyncio
from datetime import datetime, timedelta
from Hyper import Configurator

Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())
config = Configurator.cm.get_cfg()
reminder = config.others['reminder']

# 将数据存储到项目根目录的data文件夹，避免被插件加载器误识别
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "group_verify")
os.makedirs(DATA_PATH, exist_ok=True)

def get_group_config_path(gid):
    return os.path.join(DATA_PATH, f"{gid}.json")

def load_group_config(gid):
    path = get_group_config_path(gid)
    if not os.path.exists(path):
        return {
            "enabled": False,
            "verify_time": 60,
            "whitelist": []
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_group_config(gid, data):
    path = get_group_config_path(gid)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_manager(user_id):
    user_id = str(user_id)
    try:
        with open("Super_User.ini", "r") as f:
            super_users = set(line.strip() for line in f if line.strip())
    except:
        super_users = set()
    try:
        with open("Manage_User.ini", "r") as f:
            manage_users = set(line.strip() for line in f if line.strip())
    except:
        manage_users = set()
    return (
        user_id in config.others["ROOT_User"]
        or user_id in super_users
        or user_id in manage_users
    )

# 验证状态缓存: {group_id: {user_id: {"code": str, "deadline": datetime}}}
verify_cache = {}

TRIGGHT_KEYWORD = "Any"

async def on_message(event, actions, Manager, Segments):
    # 1. 处理普通消息（原有逻辑不变）
    if not hasattr(event, "message"):
        return False

    msg = str(event.message).strip()
    gid = getattr(event, "group_id", None)
    uid = getattr(event, "user_id", None)
    if not gid or not uid:
        return False

    # 权限检测
    async def check_perm():
        return is_manager(uid)

    # 开启本群人机验证
    if msg == f"{reminder}开启本群人机验证":
        if not await check_perm():
            await actions.send(group_id=gid, message=Manager.Message(Segments.Text("你没有权限操作。")))
            return True
        cfg = load_group_config(gid)
        cfg["enabled"] = True
        save_group_config(gid, cfg)
        await actions.send(group_id=gid, message=Manager.Message(Segments.Text("本群人机验证已开启。")))
        return True

    # 关闭本群人机验证
    if msg == f"{reminder}关闭本群人机验证":
        if not await check_perm():
            await actions.send(group_id=gid, message=Manager.Message(Segments.Text("你没有权限操作。")))
            return True
        cfg = load_group_config(gid)
        cfg["enabled"] = False
        save_group_config(gid, cfg)
        await actions.send(group_id=gid, message=Manager.Message(Segments.Text("本群人机验证已关闭。")))
        return True

    # 设置本群验证时间
    if msg.startswith(f"{reminder}设置本群验证时间"):
        if not await check_perm():
            await actions.send(group_id=gid, message=Manager.Message(Segments.Text("你没有权限操作。")))
            return True
        try:
            t = int(msg.replace(f"{reminder}设置本群验证时间", "").strip())
            if t < 10 or t > 600:
                raise ValueError
        except:
            await actions.send(group_id=gid, message=Manager.Message(Segments.Text("请输入10~600之间的秒数。")))
            return True
        cfg = load_group_config(gid)
        cfg["verify_time"] = t
        save_group_config(gid, cfg)
        await actions.send(group_id=gid, message=Manager.Message(Segments.Text(f"本群验证时间已设置为{t}秒。")))
        return True

    # 添加免验证
    if msg.startswith(f"{reminder}免验证"):
        if not await check_perm():
            await actions.send(group_id=gid, message=Manager.Message(Segments.Text("你没有权限操作。")))
            return True
        try:
            qq = msg.replace(f"{reminder}免验证", "").strip()
            if not qq.isdigit():
                raise ValueError
        except:
            await actions.send(group_id=gid, message=Manager.Message(Segments.Text("请输入正确的QQ号。")))
            return True
        cfg = load_group_config(gid)
        if qq not in cfg["whitelist"]:
            cfg["whitelist"].append(qq)
            save_group_config(gid, cfg)
            await actions.send(group_id=gid, message=Manager.Message(Segments.Text(f"{qq} 已加入本群免验证名单。")))
        else:
            await actions.send(group_id=gid, message=Manager.Message(Segments.Text(f"{qq} 已在免验证名单中。")))
        return True

    # 验证码输入处理
    if gid in verify_cache and uid in verify_cache[gid]:
        code = verify_cache[gid][uid]["code"]
        deadline = verify_cache[gid][uid]["deadline"]
        if datetime.now() > deadline:
            # 超时，踢出
            await actions.send(group_id=gid, message=Manager.Message([
                Segments.At(uid),
                Segments.Text("验证超时，已被移出本群。")
            ]))
            await actions.set_group_kick(group_id=gid, user_id=uid)
            del verify_cache[gid][uid]
            return True
        if msg == code:
            # 获取昵称
            try:
                info = await actions.get_group_member_info(gid, uid)
                nickname = info.data.raw.get("card") or info.data.raw.get("nickname") or str(uid)
            except:
                nickname = str(uid)
            await actions.send(group_id=gid, message=Manager.Message([
                Segments.At(uid),
                Segments.Text(f"验证通过，欢迎 {nickname} 加入本群！")
            ]))
            del verify_cache[gid][uid]
            return True
        else:
            await actions.send(group_id=gid, message=Manager.Message([
                Segments.At(uid),
                Segments.Text("验证码错误，请重新输入。")
            ]))
            return True

    # 2. 处理新成员入群事件
    from Hyper import Events
    if isinstance(event, Events.GroupMemberIncreaseEvent):
        gid = getattr(event, "group_id", None)
        uid = getattr(event, "user_id", None)
        if not gid or not uid:
            return False

        cfg = load_group_config(gid)
        if not cfg.get("enabled", False):
            return False
        if str(uid) in cfg.get("whitelist", []):
            return False

        # 生成验证码
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        verify_time = cfg.get("verify_time", 60)
        deadline = datetime.now() + timedelta(seconds=verify_time)
        if gid not in verify_cache:
            verify_cache[gid] = {}
        verify_cache[gid][uid] = {"code": code, "deadline": deadline}

        # 获取新成员昵称
        try:
            info = await actions.get_group_member_info(gid, uid)
            nickname = info.data.raw.get("card") or info.data.raw.get("nickname") or str(uid)
        except:
            nickname = str(uid)

        await actions.send(group_id=gid, message=Manager.Message([
            Segments.Text("[入群验证]\n"),
            Segments.At(uid),
            Segments.Text(f"\n请在{verify_time}秒内发送以下内容\n验证码：{code}")
        ]))

        # 定时检查
        async def check_timeout():
            await asyncio.sleep(verify_time)
            if gid in verify_cache and uid in verify_cache[gid]:
                # 超时未验证，踢出
                await actions.send(group_id=gid, message=Manager.Message([
                    Segments.At(uid),
                    Segments.Text("验证超时，已被移出本群。")
                ]))
                await actions.set_group_kick(group_id=gid, user_id=uid)
                del verify_cache[gid][uid]
        asyncio.create_task(check_timeout())

        return True

    return False

print("[GroupVerify] 入群人机验证插件已加载")