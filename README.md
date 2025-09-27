<div align="center">
  <img src="https://github.com/user-attachments/assets/4c295469-8cd8-4406-8070-6c096e15a313" alt="Jianer_QQ_Bot Logo" width="250">
  
  # 小依 QQ 机器人 (Xiaoyi_QQ)
  ### Demo - 全新QQ机器人框架
  
  <p>基于 NTQQ 的智能开源机器人 · 插件化架构 · AI多模型支持 · 工作流自动化</p>

  <p>
    <img src="https://img.shields.io/badge/OneBot-11-black?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYLBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==" alt="Badge">
    <img src="https://img.shields.io/badge/Language-Python-coral" alt="Language">  
    <img src="https://img.shields.io/badge/Version-3.0_Demo-blue" alt="Version" />
    <img src="https://img.shields.io/badge/license-AGPL--3.0-blue" alt="License" />
    <img src="https://img.shields.io/badge/Framework-HypeR_Bot-orange" alt="Framework" />
  </p>
</div>

## ✨ 核心特性

### 🤖 多AI模型支持
- **插件支持** - 插件化架构，支持自定义插件，高可定制性
- **智能切换** - AI插件管理系统可以通过指令调取不同AI插件
- **记忆管理** - 通过独立的记忆管理系统，实现长对话记忆，多人对话和独立对话分离

### 🔧 插件生态
- **内置插件** - 覆盖娱乐、工具、管理等多个领域
- **模块化设计** - 支持热重载，无需重启
- **自定义API** - 灵活的API接口，支持外部服务集成
- **插件管理器** - 可视化插件管理界面

### 🎯 工作流自动化
- **可视化配置** - 可视化工作流设计
- **高自定义** - 通过大量可用变量精确匹配流程
- **事件触发** - 基于消息、时间等事件的自动化

### 🎨 现代化界面
- **设置向导** - 图形化配置界面
- **WebUI** - 基于Web的管理后台
- **实时监控** - 机器人状态和日志监控
- **诊断工具** - 我们编写了多个修复工具用来自动修复部署时可能出现的错误

## 🚀 快速开始

### 安装要求
- Python 3.8+（开发环境为 Python 3.13）
- Windows 10/11（作为主流系统/Linux也可部署）
- 2GB+ RAM

### 待完善
- 部署教程

## 🛠️ 修复工具
#### 记忆问题
```bash
# 诊断记忆状态
python test_group_notice.py
```

#### AI服务问题
```bash
# 测试AI连接
python test_ai_memory.py

# 切换AI模型
# 使用配置向导重新配置
```

#### 工作流问题
```bash
# 测试工作流
python test_workflow.py
```

### 获取帮助

- 📖 查看 [使用文档](./docs/)
- 🐛 提交 [Issue](https://github.com/YourRepo/issues)
- 💬 加入 [QQ交流群]()
- 📧 邮件联系: 2477194503@qq.com


## 🤝 贡献指南

我们欢迎任何形式的贡献！无论是新功能、Bug修复、文档改进还是插件开发。

### 🚀 快速参与

1. **Fork本项目**
   ```bash
   git clone https://github.com/ValkyrieEY/Xiaoyi_QQ.git
   ```

2. **创建功能分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **提交更改**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

4. **推送分支**
   ```bash
   git push origin feature/amazing-feature
   ```

### 🏆 贡献者

感谢所有为项目做出贡献的开发者！

<a href="https://github.com/ValkyrieEY/Xiaoyi_QQ/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ValkyrieEY/Xiaoyi_QQ" />
</a>

### 🎖️ 特别感谢

- [SRInternet-Studio](https://github.com/SRInternet-Studio/Jianer_QQ_bot) - 提供基础框架
- [LagrangeDev](https://github.com/LagrangeDev/Lagrange.Core) - OneBot协议实现
- [HypeR_Bot](https://github.com/HarcicYang/HypeR_Bot) - 机器人框架支持

## 📝 开源协议

本项目基于 [AGPL-3.0](LICENSE) 协议开源。

使用本项目时请遵守以下要求：
- 保留原始作者信息和版权声明
- 任何基于本项目的衍生作品也必须开源
- 商业使用需要遵守AGPL-3.0协议条款
- 网络服务提供必须提供源代码

## 💬 联系我们

### 🔗 官方链接

- 🏠 **项目主页**: [GitHub Repository](https://github.com/ValkyrieEY/Xiaoyi_QQ)
- 📚 **使用文档**: [项目Wiki](https://github.com/ValkyrieEY/Xiaoyi_QQ/wiki)
- 🐛 **问题反馈**: [Issues页面](https://github.com/ValkyrieEY/Xiaoyi_QQ/issues)
- 🔄 **项目发布**: [Releases页面](https://github.com/ValkyrieEY/Xiaoyi_QQ/releases)

### 👥 社区交流

- 💬 **QQ交流群**: [点击加入]()
- 📧 **邮箱联系**: 2477194503@qq.com
- 🌐 **技术博客**: [依の技术栈](https://xun.eynet.top/)

### ⭐ 支持项目

如果这个项目对你有帮助，请考虑：

- ⭐ 给项目点个Star
- 🍴 Fork项目并参与开发
- 📝 帮助完善文档
- 🐛 报告Bug和问题
- 💡 提出新功能建议
- 📢 推荐给其他开发者

---

<div align="center">

### 🎯 项目统计

<img src="https://img.shields.io/github/stars/ValkyrieEY/Xiaoyi_QQ?style=social" alt="GitHub stars">
<img src="https://img.shields.io/github/forks/ValkyrieEY/Xiaoyi_QQ?style=social" alt="GitHub forks">
<img src="https://img.shields.io/github/watchers/ValkyrieEY/Xiaoyi_QQ?style=social" alt="GitHub watchers">

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ValkyrieEY/Xiaoyi_QQ)
![GitHub last commit](https://img.shields.io/github/last-commit/ValkyrieEY/Xiaoyi_QQ)
![GitHub contributors](https://img.shields.io/github/contributors/ValkyrieEY/Xiaoyi_QQ)

**✨ 小依 QQ 机器人 - NTQQ Robot ✨**

**Xiaoyi QQ Bot** ©2024 Created by ValkyrieEY & Xiaoyi

*Built with ❤️ by the open source community*

</div>
