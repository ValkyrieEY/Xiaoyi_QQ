from Hyper import Configurator
import httpx
import re

Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

API_URL = "https://api.yuafeng.cn/API/ly/dyjx.php?url={}"

TRIGGHT_KEYWORD = "Any"

async def on_message(event, actions, Manager, Segments):
    if not hasattr(event, "message"):
        return False
    message_content = str(event.message).strip()
    match = re.search(r'(https?://v\.douyin\.com/[^\s]+)', message_content)
    if not match:
        return False

    douyin_url = match.group(1)
    api_url = API_URL.format(douyin_url)

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(api_url, timeout=10.0)
            data = resp.json()
    except Exception as e:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(f"抖音解析失败: {e}"))
        )
        return True

    if data.get("code") != 0 or "data" not in data:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(f"抖音解析失败: {data.get('msg', '未知错误')}"))
        )
        return True

    info = data["data"]

    # 1. 发送作者信息
    author = info.get("author", {})
    author_msg = [
        Segments.Image(author.get("avatar", "")),
        Segments.Text(f"\n作者昵称：{author.get('name', '')}\n"
            f"抖音号：{author.get('id', '')}\n"
            f"签名：{author.get('signature', '')}"
        )
    ]
    await actions.send(
        group_id=event.group_id,
        message=Manager.Message(author_msg)
    )

    # 2. 发送视频信息
    music = info.get("music", {})
    count = info.get("count", {})
    desc = info.get('desc', '')
    desc = re.sub(r'[\r\n]+', ' ', desc)
    video_url = info.get('url', '')

    video_msg = [
        Segments.Image(info.get("cover", "")),
        Segments.Text(f"\n简介：{desc}\n"
            f"标签：{info.get('tag', '')}\n"
            f"音乐：{music.get('title', '')}（作者：{music.get('author', '')}，时长：{music.get('duration', '')}秒）\n"
            f"👍点赞：{count.get('like', 0)}  💬评论：{count.get('comment', 0)}  📢分享：{count.get('share', 0)}  ⭐收藏：{count.get('collect', 0)}\n"
            f"🔗视频直链：{video_url}"
        )
    ]
    await actions.send(
        group_id=event.group_id,
        message=Manager.Message(video_msg)
    )

    # 3. 发送视频文件（如果支持 Segments.Video）
    if video_url:
        try:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message([Segments.Video(video_url)])
            )
        except Exception as e:
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"视频发送失败：{e}"))
            )

    return True

print("[Xiaoyi_QQ]抖音解析插件已加载")