from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
from typing import Dict, Optional, Tuple
from .config import config

class BaseTemplate:
    def __init__(self, template_name: str = "default"):
        self.template_config = config.TEMPLATE_CONFIG[template_name]
        self.width = self.template_config["width"]
        self.height = self.template_config["height"]
        self.padding = self.template_config["padding"]
        self.line_height = self.template_config["line_height"]
        self.font_size = self.template_config["font_size"]
        self.bg_color = self.template_config["bg_color"]
        self.text_color = self.template_config["text_color"]
        self.section_color = self.template_config["section_color"]
        self.show_avatar = self.template_config["show_avatar"]
        self.show_bg = self.template_config["show_bg"]
        
        try:
            self.font = ImageFont.truetype("arial.ttf", self.font_size)
        except:
            self.font = ImageFont.load_default()
    
    def draw_text(self, draw: ImageDraw.ImageDraw, text: str, x: int, y: int, color: Optional[Tuple[int, int, int]] = None) -> int:
        """绘制文本"""
        if color is None:
            color = self.text_color
        draw.text((x, y), text, fill=color, font=self.font)
        return y + self.line_height
    
    def draw_section(self, draw: ImageDraw.ImageDraw, title: str, y: int) -> int:
        """绘制分区标题"""
        draw.text((self.padding, y), f"=== {title} ===", fill=self.section_color, font=self.font)
        return y + self.line_height
    
    def draw_system_info(self, draw: ImageDraw.ImageDraw, info: Dict, y: int) -> int:
        """绘制系统信息"""
        y = self.draw_section(draw, "系统信息", y)
        y = self.draw_text(draw, f"系统: {info['system']} {info['release']}", self.padding, y)
        y = self.draw_text(draw, f"版本: {info['version']}", self.padding, y)
        y = self.draw_text(draw, f"启动时间: {info['boot_time']}", self.padding, y)
        y = self.draw_text(draw, f"运行时间: {info['uptime']}", self.padding, y)
        return y + self.line_height
    
    def draw_cpu_info(self, draw: ImageDraw.ImageDraw, info: Dict, y: int) -> int:
        """绘制CPU信息"""
        y = self.draw_section(draw, "CPU信息", y)
        y = self.draw_text(draw, f"使用率: {info['percent']}%", self.padding, y)
        y = self.draw_text(draw, f"核心数: {info['count']}", self.padding, y)
        if info['freq']:
            y = self.draw_text(draw, f"频率: {info['freq']}MHz", self.padding, y)
        return y + self.line_height
    
    def draw_memory_info(self, draw: ImageDraw.ImageDraw, info: Dict, y: int) -> int:
        """绘制内存信息"""
        y = self.draw_section(draw, "内存信息", y)
        y = self.draw_text(draw, f"使用率: {info['percent']}%", self.padding, y)
        y = self.draw_text(draw, f"总量: {info['total']}GB", self.padding, y)
        y = self.draw_text(draw, f"已用: {info['used']}GB", self.padding, y)
        return y + self.line_height
    
    def draw_disk_info(self, draw: ImageDraw.ImageDraw, disks: list, y: int) -> int:
        """绘制磁盘信息"""
        y = self.draw_section(draw, "磁盘信息", y)
        for disk in disks:
            y = self.draw_text(draw, f"设备: {disk['device']}", self.padding, y)
            y = self.draw_text(draw, f"挂载点: {disk['mountpoint']}", self.padding, y)
            y = self.draw_text(draw, f"使用率: {disk['percent']}%", self.padding, y)
            y = self.draw_text(draw, f"总量: {disk['total']}GB", self.padding, y)
            y = self.draw_text(draw, f"已用: {disk['used']}GB", self.padding, y)
            y += self.line_height
        return y
    
    def draw_network_info(self, draw: ImageDraw.ImageDraw, nets: list, y: int) -> int:
        """绘制网络信息"""
        y = self.draw_section(draw, "网络信息", y)
        for net in nets:
            y = self.draw_text(draw, f"接口: {net['name']}", self.padding, y)
            y = self.draw_text(draw, f"发送: {net['bytes_sent']}MB", self.padding, y)
            y = self.draw_text(draw, f"接收: {net['bytes_recv']}MB", self.padding, y)
            y += self.line_height
        return y
    
    def draw_process_info(self, draw: ImageDraw.ImageDraw, processes: list, y: int) -> int:
        """绘制进程信息"""
        y = self.draw_section(draw, "进程信息", y)
        for proc in processes:
            y = self.draw_text(draw, f"PID: {proc['pid']} - {proc['name']}", self.padding, y)
            y = self.draw_text(draw, f"CPU: {proc['cpu_percent']}% | 内存: {proc['memory_percent']}%", self.padding, y)
            y += self.line_height
        return y
    
    def draw_network_test(self, draw: ImageDraw.ImageDraw, tests: list, y: int) -> int:
        """绘制网络测试信息"""
        y = self.draw_section(draw, "网络测试", y)
        for test in tests:
            status_color = (0, 255, 0) if test['status'] == "正常" else (255, 0, 0)
            y = self.draw_text(draw, f"{test['name']}: {test['status']}", self.padding, y, status_color)
            if test['time'] > 0:
                y = self.draw_text(draw, f"响应时间: {test['time']}ms", self.padding, y)
            y += self.line_height
        return y
    
    def apply_background(self, image: Image.Image, bg_image: Optional[bytes] = None) -> Image.Image:
        """应用背景"""
        if self.show_bg and bg_image:
            try:
                bg = Image.open(io.BytesIO(bg_image))
                bg = bg.resize((self.width, self.height))
                # 调整背景透明度
                bg = ImageEnhance.Brightness(bg).enhance(0.7)
                # 合并图片
                image = Image.alpha_composite(bg.convert('RGBA'), image.convert('RGBA'))
            except:
                pass
        return image
    
    def apply_avatar(self, image: Image.Image, avatar: Optional[bytes] = None) -> Image.Image:
        """应用头像"""
        if self.show_avatar and avatar:
            try:
                avatar_img = Image.open(io.BytesIO(avatar))
                avatar_img = avatar_img.resize((100, 100))
                # 在右上角添加头像
                image.paste(avatar_img, (self.width - 120, 20))
            except:
                pass
        return image
    
    def render(self, info: Dict, bg_image: Optional[bytes] = None, avatar: Optional[bytes] = None) -> bytes:
        """渲染状态图片"""
        # 创建图片
        image = Image.new('RGBA', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(image)
        y = self.padding
        
        # 绘制各个部分
        y = self.draw_system_info(draw, info['system'], y)
        y = self.draw_cpu_info(draw, info['cpu'], y)
        y = self.draw_memory_info(draw, info['memory'], y)
        y = self.draw_disk_info(draw, info['disk'], y)
        y = self.draw_network_info(draw, info['network'], y)
        y = self.draw_process_info(draw, info['process'], y)
        y = self.draw_network_test(draw, info['network_test'], y)
        
        # 应用背景和头像
        image = self.apply_background(image, bg_image)
        image = self.apply_avatar(image, avatar)
        
        # 转换为字节流
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()

class TemplateManager:
    def __init__(self):
        self.templates = {}
        self.current_template = None
    
    def register_template(self, name: str, template_class: type):
        """注册模板"""
        self.templates[name] = template_class
    
    def get_template(self, name: str = None) -> BaseTemplate:
        """获取模板实例"""
        if name is None:
            name = config.TEMPLATE
        if name not in self.templates:
            name = "default"
        if self.current_template is None or self.current_template.__class__ != self.templates[name]:
            self.current_template = self.templates[name](name)
        return self.current_template

# 创建模板管理器
template_manager = TemplateManager()

# 注册默认模板
template_manager.register_template("default", BaseTemplate)
template_manager.register_template("simple", BaseTemplate)
template_manager.register_template("modern", BaseTemplate)

# 导出模板实例
template = template_manager.get_template() 