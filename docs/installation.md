# 📦 安装部署指南

## 📋 系统要求

### 基础环境
- **Python版本**: 3.8+ (推荐 Python 3.13)
- **操作系统**: Windows 10/11 (主要支持) / Linux (也可部署)
- **内存要求**: 2GB+ RAM
- **存储空间**: 500MB+ 可用空间

### 依赖环境
- NTQQ 客户端
- OneBot 11 协议支持
- 网络连接 (用于AI服务和在线功能)

## 🚀 安装步骤

### 1. 克隆项目
```bash
git clone https://github.com/ValkyrieEY/Xiaoyi_QQ.git
cd Xiaoyi_QQ
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境
```bash
# 运行配置向导
python SetupWizard.py
```

### 4. 首次启动
```bash
# 启动机器人
python main.py
```

## ⚙️ 配置说明

### 基础配置
- **机器人账号**: 配置QQ机器人账号信息
- **OneBot连接**: 设置OneBot协议连接参数
- **插件目录**: 指定插件加载路径

### AI配置
- **AI适配器**: 配置支持的AI模型
- **API密钥**: 设置各AI服务的API密钥
- **模型参数**: 调整AI响应参数

## 🔧 常见问题

### Q: Python版本不兼容？
A: 请确保使用Python 3.8+版本，推荐使用Python 3.13

### Q: 依赖安装失败？
A: 尝试使用以下命令：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: OneBot连接失败？
A: 检查NTQQ客户端是否正常运行，OneBot插件是否正确安装

## 📱 Docker部署

### Docker安装
```bash
# 构建镜像
docker build -t xiaoyi-qq .

# 运行容器
docker run -d --name xiaoyi-qq-bot xiaoyi-qq
```

### Docker Compose
```yaml
version: '3.8'
services:
  xiaoyi-qq:
    build: .
    container_name: xiaoyi-qq-bot
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    restart: unless-stopped
```

## 🛠️ 高级配置

### 环境变量
```bash
# 设置工作目录
export XIAOYI_WORK_DIR=/path/to/xiaoyi

# 设置日志级别
export XIAOYI_LOG_LEVEL=INFO

# 设置AI模型
export XIAOYI_DEFAULT_AI=deepseek
```

### 配置文件
- `appsettings.json` - 主配置文件
- `config/ai_adapters.json` - AI适配器配置
- `config/workflow_config.json` - 工作流配置

## 🔄 更新升级

### 从Git更新
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### 版本迁移
在重大版本更新时，请查看 [更新日志](./changelog.md) 了解迁移步骤。

## 🆘 获取帮助

如果在安装过程中遇到问题：

1. 查看 [常见问题](./faq.md)
2. 运行诊断工具: `python fix_build_issues.py`
3. 提交 [Issue](https://github.com/ValkyrieEY/Xiaoyi_QQ/issues)
4. 加入QQ交流群获取技术支持