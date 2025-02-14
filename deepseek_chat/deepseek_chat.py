import asyncio
import json
import traceback
from collections import defaultdict
from typing import Dict, List
import aiohttp
from Hyper import Configurator
if not hasattr(Configurator, 'cm'):
    Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

from Hyper import Configurator, Segments, Manager
from Hyper.Events import GroupMessageEvent

class MemorySystem:
    def __init__(self):
        # 使用嵌套字典存储记忆：{group_id: {user_id: history}}
        self.history: Dict[int, Dict[int, List[dict]]] = defaultdict(lambda: defaultdict(list))
        self.max_history = 5  # 保留最近5轮对话
        self.max_tokens = 2048  # 最大token限制

    def _trim_history(self, history: List[dict]) -> List[dict]:
        """修剪历史记录，确保不超过限制"""
        total_len = sum(len(msg["content"]) for msg in history)
        while len(history) > 1 and total_len > self.max_tokens:
            removed = history.pop(0)
            total_len -= len(removed["content"])
        return history

    def get_history(self, group_id: int, user_id: int) -> List[dict]:
        return self.history[group_id][user_id]

    def add_message(self, group_id: int, user_id: int, role: str, content: str):
        history = self.history[group_id][user_id]
        history.append({"role": role, "content": content})
        self._trim_history(history)

    def clear_history(self, group_id: int, user_id: int):
        self.history[group_id][user_id].clear()

class DeepSeekChat:
    def __init__(self):
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.config = Configurator.cm.get_cfg()
        self.token = self.config.others.get("deepseek_key", "")
        self.headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.retries = 2
        self.memory = MemorySystem()

    async def _build_payload(self, group_id: int, user_id: int, question: str) -> dict:
        # 获取历史记录并添加新问题
        history = self.memory.get_history(group_id, user_id)
        history.append({"role": "user", "content": question})
        
        return {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": history[-5:],  # 只保留最近5轮对话
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7
        }

    async def get_response(self, group_id: int, user_id: int, question: str) -> str:
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            for attempt in range(self.retries + 1):
                try:
                    payload = await self._build_payload(group_id, user_id, question)
                    
                    async with session.post(self.api_url, json=payload, headers=self.headers) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            reply = result["choices"][0]["message"]["content"].strip()
                            
                            # 保存到记忆系统
                            self.memory.add_message(group_id, user_id, "user", question)
                            self.memory.add_message(group_id, user_id, "assistant", reply)
                            return reply
                        
                        # 错误处理...（保持原有错误处理逻辑）

                except Exception as e:
                    # 错误处理...（保持原有错误处理逻辑）
                    pass

async def on_message(event: GroupMessageEvent, actions) -> str:
    msg = str(event.message).strip()
    
    # 处理清除记忆命令
    if msg.lower() == "671b 清除记忆":
        ds = DeepSeekChat()
        ds.memory.clear_history(event.group_id, event.user_id)
        return "✅ 已清除对话历史"
    
    if not msg.startswith("671b "):
        return ""

    question = msg[len("671b "):].strip()
    if not question:
        return "请输入要咨询的问题"

    # 显示等待提示
    notice = await actions.send(
        group_id=event.group_id,
        message=Manager.Message(Segments.Text("⌛ 正在查询深度记忆库（最近5轮对话）..."))
    )
    try:
        ds = DeepSeekChat()
        response = await ds.get_response(event.group_id, event.user_id, question)
        
        # 格式化响应
        history_count = len(ds.memory.get_history(event.group_id, event.user_id)) // 2
        formatted_response = f"🔍 DeepSeek回复（基于{history_count}轮历史）：\n{response}"
        
        await actions.del_message(notice.data["message_id"])
    except Exception as e:
        formatted_response = f"❌ 记忆库访问失败：{str(e)}"
    
    return formatted_response
