# WebScreenshot 网页截图插件

## 插件信息
- 名称: WebScreenshot
- 版本: 1.2.0
- 作者: Xiaoyi

## 功能简介
WebScreenshot 是一个强大的网页截图插件，支持自动识别消息中的 URL 并进行网页长截图，同时提供手动触发功能和性能优化配置。

## 主要特性
- 自动识别 URL 并截图
- 支持手动触发截图
- 智能资源管理
- 并发控制和限流
- 自动清理临时文件
- 支持长截图

## 使用方法

### 自动截图
直接在消息中发送 URL，插件会自动识别并截图:
```
https://www.example.com
```

### 手动命令
1. 手动触发截图:
```
!ws url https://www.example.com
```

2. 查看帮助:
```
!ws help
```

## 技术规格

### 性能配置
```json
{
    "max_concurrent": 1,      // 最大并发数
    "min_interval": 5,        // 最小间隔(秒)
    "timeout": 15000,         // 超时时间(毫秒)
    "max_height": 15000,      // 最大高度(像素)
    "viewport_width": 1280,   // 视口宽度
    "viewport_height": 720,   // 视口高度
    "image_quality": 70       // 图片质量
}
```

### 截图目录
```
./screenshots/
```

## 限制说明
1. 每个用户有 5 秒冷却时间
2. 每条消息最多处理 2 个 URL
3. 最大截图高度 15000 像素
4. 并发限制为 1

## 错误处理
- URL 格式无效提示
- 操作频率限制提示
- 截图失败提示
- 服务器繁忙提示

## 依赖项
- playwright
- asyncio
- Hyper 框架
- Python 3.7+

## 安装要求
1. 安装 Python 依赖:
```bash
pip install playwright
playwright install chromium
```

2. 确保系统环境:
- Windows/Linux/MacOS
- 足够的磁盘空间
- 稳定的网络连接

## 技术实现
- 异步处理
- 浏览器自动化
- 资源自动清理
- 智能限流控制

## 注意事项
1. 确保有适当的磁盘权限
2. 保持网络连接稳定
3. 注意 URL 格式正确
4. 避免频繁操作

## 更新日志
### v1.2.0
- 添加并发控制
- 优化资源管理
- 改进错误处理
- 添加自动清理功能

### v1.1.0
- 添加手动触发功能
- 改进 URL 识别
- 增加帮助命令

### v1.0.0
- 初始版本发布
- 基础截图功能