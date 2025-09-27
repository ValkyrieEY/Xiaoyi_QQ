from Hyper import Configurator
import httpx
import re
import json
import os
import time
import hashlib
from urllib.parse import quote
import asyncio

# 加载配置
Configurator.cm = Configurator.ConfigManager(Configurator.Config(file="config.json").load_from_file())

# 插件信息
TRIGGHT_KEYWORD = "绘画"
HELP_MESSAGE = f"""{Configurator.cm.get_cfg().others['reminder']}绘画 [描述文本] -> 让AI帮你画一张图
    {Configurator.cm.get_cfg().others['reminder']}切换绘画接口 -> 在不同绘画API间切换"""

class AIDrawAPI:
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url

class AIDrawManager:
    def __init__(self):
        # 将数据存储到项目根目录的data文件夹，避免被插件加载器误识别
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "aidraw")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # API配置
        self.apis = {
            "pollinations": {
                "name": "Pollinations",
                "url": "https://image.pollinations.ai/prompt/"
            },
            "yjai": {
                "name": "YJAI", 
                "url": "http://api.yjai.art:8080/painting-open-api"
            }
        }
        
        # 添加密钥文件路径
        self.keys_file = os.path.join(self.data_dir, "yjai_keys.json")
        self.keys = self._load_keys()
        
        # 加载配置文件
        self.config_file = os.path.join(self.data_dir, "config.json")
        self.config = self._load_config()
        
        # 设置当前API时直接使用字典存储
        self.current_api = self.config.get("current_api", "pollinations")
        print(f"[AI绘画]当前使用API: {self.apis[self.current_api]['name']}")

    def _load_keys(self) -> dict:
        """加载YJAI密钥"""
        if not os.path.exists(self.keys_file):
            default_keys = {
                "yjai_key": "",  # 你的YJAI API key
                "yjai_secret": ""  # 你的YJAI API secret
            }
            with open(self.keys_file, "w", encoding="utf-8") as f:
                json.dump(default_keys, f, ensure_ascii=False, indent=2)
            return default_keys
        with open(self.keys_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_config(self) -> dict:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            default_config = {
                "current_api": "pollinations"
            }
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            return default_config
        with open(self.config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_config(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def switch_api(self) -> str:
        """切换到下一个API"""
        api_list = list(self.apis.keys())
        current_index = api_list.index(self.current_api)
        next_index = (current_index + 1) % len(api_list)
        self.current_api = api_list[next_index]
        
        # 保存配置
        self.config["current_api"] = self.current_api
        self._save_config()
        
        return f"已切换至 {self.apis[self.current_api]['name']} API"

    def _generate_yjai_sign(self, params: dict) -> str:
        """生成YJAI API签名"""
        params["apikey"] = self.keys["yjai_key"]
        params["apisecret"] = self.keys["yjai_secret"]
        params["timestamp"] = str(int(time.time()))
        
        # 按键排序
        sorted_params = sorted(params.items())
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        
        # 计算MD5
        return hashlib.md5(sign_str.encode()).hexdigest()

    async def generate_image_yjai(self, prompt: str) -> tuple[str | None, str | None]:
        """使用YJAI API生成图像"""
        try:
            # 检查API密钥是否配置
            if not self.keys["yjai_key"] or not self.keys["yjai_secret"]:
                return None, "YJAI API密钥未配置"
            
            # 构建请求参数
            params = {
                "task_num": 1,
                "prompt": prompt,
                "engine": "stable_diffusion",
                "apikey": self.keys["yjai_key"],
                "timestamp": str(int(time.time()))
            }
            
            # 生成签名
            sign = self._generate_yjai_sign(params)
            
            # 发送请求
            headers = {"sign": sign}
            async with httpx.AsyncClient(timeout=30.0) as client:
                print(f"[AI绘画]发起YJAI绘图请求: {prompt}")
                response = await client.post(
                    f"{self.apis['yjai']['url']}/site/v2/draw/put_batch_task",
                    headers=headers,
                    data=params
                )
                
                data = response.json()
                print(f"[AI绘画]YJAI响应: {data}")
                
                if data["status"] != 0:
                    return None, f"API错误: {data.get('reason', '未知错误')}"
                    
                task_id = data["data"]["TaskIds"][0]
                print(f"[AI绘画]YJAI任务ID: {task_id}")
                
                # 轮询任务状态
                for i in range(30):
                    status_params = {
                        "uuid": task_id,
                        "apikey": self.keys["yjai_key"],
                        "timestamp": str(int(time.time()))
                    }
                    status_sign = self._generate_yjai_sign(status_params)
                    
                    print(f"[AI绘画]查询YJAI任务状态 {i+1}/30")
                    status_response = await client.post(
                        f"{self.apis['yjai']['url']}/site/show_task_detail",
                        headers={"sign": status_sign},
                        data=status_params
                    )
                    
                    status_data = status_response.json()
                    print(f"[AI绘画]状态查询响应: {status_data}")
                    
                    # 检查错误状态
                    if status_data["status"] != 0:
                        print(f"[AI绘画]查询任务状态失败: {status_data['reason']}")
                        await asyncio.sleep(2)
                        continue
                    
                    # 确保data字段存在且不为空
                    if not status_data.get("data"):
                        print("[AI绘画]等待任务开始...")
                        await asyncio.sleep(2)
                        continue
                    
                    task_status = status_data["data"].get("Status")
                    print(f"[AI绘画]当前任务状态: {task_status}")
                    
                    if task_status == 1:  # 完成
                        image_url = status_data["data"]["ImageUrls"][0]
                        print(f"[AI绘画]获取到图片URL: {image_url}")
                        
                        image_response = await client.get(image_url)
                        timestamp = int(time.time())
                        filename = f"draw_{timestamp}.png"
                        filepath = os.path.join(self.data_dir, filename)
                        
                        with open(filepath, "wb") as f:
                            f.write(image_response.content)
                        
                        print(f"[AI绘画]图片已保存: {filepath}")    
                        return filepath, None
                        
                    elif task_status in [3, 4]:  # 失败或取消
                        return None, "任务失败或被取消"
                        
                    await asyncio.sleep(2)
                    
                return None, "等待超时"
                
        except Exception as e:
            print(f"[AI绘画]YJAI绘图错误: {str(e)}")
            return None, f"生成图片失败: {str(e)}"

    async def generate_image(self, prompt: str) -> tuple[str | None, str | None]:
        """根据当前API生成图像"""
        if self.current_api == "pollinations":
            try:
                encoded_prompt = quote(prompt)
                image_url = f"{self.apis['pollinations']['url']}{encoded_prompt}"
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(image_url)
                    response.raise_for_status()
                    
                    timestamp = int(time.time())
                    filename = f"draw_{timestamp}.png"
                    filepath = os.path.join(self.data_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    
                    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                        return filepath, None
                    return None, "图片保存失败或文件大小为0"
                    
            except Exception as e:
                return None, f"生成图片失败: {str(e)}"
        else:
            return await self.generate_image_yjai(prompt)

draw_manager = AIDrawManager()

async def on_message(event, actions, Manager, Segments):
    if not hasattr(event, 'message'):
        return False
        
    message = str(event.message).strip()
    reminder = Configurator.cm.get_cfg().others["reminder"]
    
    # 处理切换API命令
    if message == f"{reminder}切换绘画接口":
        result = draw_manager.switch_api()
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(result))
        )
        return True
    
    # 如果不是绘画命令，直接返回False让主程序处理
    if not message.startswith(f"{reminder}绘画 "):
        return False
    
    # 提取描述文本
    prompt = message[len(f"{reminder}绘画 "):].strip()
    if not prompt:
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text("请输入要绘制的内容描述"))
        )
        return True
    
    # 发送等待消息
    await actions.send(
        group_id=event.group_id,
        message=Manager.Message(Segments.Text("正在绘制中，请稍候..."))
    )
    
    try:
        # 直接使用用户输入的提示词
        filepath, error = await draw_manager.generate_image(prompt)
        if error:
            print(f"[Xiaoyi_QQAI绘画]生成错误: {error}")
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(error))
            )
            return True
            
        print(f"[Xiaoyi_QQAI绘画]准备发送图片: {filepath}")
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"图片文件不存在: {filepath}")
                
            file_size = os.path.getsize(filepath)
            print(f"[Xiaoyi_QQAI绘画]图片大小: {file_size} 字节")
            
            # 构建消息
            message = Manager.Message([
                Segments.Text(f"已完成绘制: {prompt}\n"),
                Segments.Image(f"file:///{filepath}")
            ])
            
            print("[Xiaoyi_QQAI绘画]开始发送消息...")
            await actions.send(
                group_id=event.group_id,
                message=message
            )
            print("[Xiaoyi_QQAI绘画]消息发送完成")
            
        except Exception as e:
            print(f"[Xiaoyi_QQAI绘画]发送消息失败: {str(e)}")
            await actions.send(
                group_id=event.group_id,
                message=Manager.Message(Segments.Text(f"发送图片失败: {str(e)}"))
            )
        finally:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"[Xiaoyi_QQAI绘画]已清理临时文件: {filepath}")
            except Exception as e:
                print(f"[Xiaoyi_QQAI绘画]清理文件失败: {str(e)}")
            
        return True
        
    except Exception as e:
        print(f"[Xiaoyi_QQAI绘画]处理过程出错: {str(e)}")
        await actions.send(
            group_id=event.group_id,
            message=Manager.Message(Segments.Text(f"绘制过程出错: {str(e)}"))
        )
        return True

print("[Xiaoyi_QQ]AI绘画插件已加载")