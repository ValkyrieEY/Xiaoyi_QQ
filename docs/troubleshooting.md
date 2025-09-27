# 🛠️ 故障排除指南

## 🔍 常见问题诊断

### 自动诊断工具
```bash
# 运行完整诊断
python fix_build_issues.py

# WebSocket连接诊断
python fix_websocket_issue.py

# AI记忆系统测试
python test_ai_memory.py

# 群组通知测试
python test_group_notice.py
```

## 🚨 启动问题

### Q1: Python版本不兼容
**症状**: `SyntaxError` 或版本警告
**解决方案**:
```bash
# 检查Python版本
python --version

# 如果版本低于3.8，请升级Python
# Windows: 从官网下载最新版本
# Linux: sudo apt update && sudo apt install python3.13
```

### Q2: 依赖安装失败
**症状**: `ModuleNotFoundError` 或 `ImportError`
**解决方案**:
```bash
# 使用国内镜像安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 强制重新安装
pip install -r requirements.txt --force-reinstall

# 升级pip
python -m pip install --upgrade pip
```

### Q3: 配置文件错误
**症状**: `JSON decode error` 或配置加载失败
**解决方案**:
```bash
# 验证JSON格式
python -c "import json; json.load(open('appsettings.json'))"

# 重置配置文件
cp appsettings.json.template appsettings.json

# 运行配置向导
python launcher.py
```

## 🔌 连接问题

### OneBot连接失败
**症状**: 无法连接到NTQQ
**诊断步骤**:
1. 检查NTQQ是否正常运行
2. 验证OneBot插件是否正确安装
3. 检查端口是否被占用
4. 验证WebSocket连接

```bash
# 检查端口占用
netstat -an | findstr :8080

# 测试WebSocket连接
python websocket_diagnosis.py
```

**解决方案**:
```bash
# 重启NTQQ和OneBot
# 修改端口配置
# 检查防火墙设置
```

### 网络连接问题
**症状**: API调用超时或失败
**解决方案**:
```bash
# 测试网络连接
ping api.deepseek.com
ping generativelanguage.googleapis.com

# 检查代理设置
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 配置代理（如需要）
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port
```

## 🤖 AI服务问题

### API密钥无效
**症状**: `401 Unauthorized` 或 `403 Forbidden`
**解决方案**:
1. 验证API密钥是否正确
2. 检查API配额是否充足
3. 确认API服务状态

```bash
# 测试DeepSeek API
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.deepseek.com/v1/models

# 测试Gemini API  
curl -H "Content-Type: application/json" \
     "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY"
```

### AI响应缓慢
**症状**: AI回复时间过长
**优化方案**:
```json
// 调整AI参数 - config/ai_adapters.json
{
  "deepseek": {
    "max_tokens": 1000,        // 减少token数量
    "temperature": 0.7,        // 降低创造性
    "timeout": 15              // 设置超时时间
  }
}
```

### 记忆系统问题
**症状**: 对话记忆丢失或错误
**解决方案**:
```bash
# 清理记忆数据
rm -rf data/memory/

# 重建记忆索引
python test_ai_memory.py --rebuild

# 检查存储权限
ls -la data/
```

## 🔌 插件问题

### 插件加载失败
**症状**: 插件无法正常工作
**诊断步骤**:
```bash
# 检查插件语法
python -m py_compile plugins/plugin_name.py

# 测试插件导入
python -c "from plugins import plugin_name"

# 查看详细错误
python main.py --debug
```

### 插件权限问题
**症状**: 插件功能受限
**解决方案**:
1. 检查用户权限配置
2. 验证群组白名单设置
3. 确认插件配置文件

```json
// 检查插件配置
{
  "enabled": true,
  "permissions": {
    "users": ["123456"],
    "groups": ["789012"], 
    "admin_only": false
  }
}
```

## 📊 性能问题

### 内存使用过高
**症状**: 系统内存不足
**优化方案**:
```python
# 调整记忆配置
MEMORY_CONFIG = {
    "max_history": 20,      # 减少历史记录
    "context_window": 5,    # 缩小上下文窗口
    "memory_decay": 0.2     # 增加衰减率
}
```

### CPU使用率高
**症状**: 系统响应缓慢
**优化方案**:
1. 减少并发处理数量
2. 优化正则表达式
3. 使用缓存机制

```python
# 添加缓存装饰器
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_function(param):
    # 耗时操作
    pass
```

## 🗃️ 数据问题

### 数据库连接失败
**症状**: 数据存储错误
**解决方案**:
```bash
# 检查数据目录权限
chmod 755 data/
chmod 644 data/*.json

# 备份重要数据
cp -r data/ data_backup_$(date +%Y%m%d)/

# 重建数据结构
python -c "from tools import init_data_structure; init_data_structure()"
```

### 配置文件损坏
**症状**: JSON解析错误
**修复步骤**:
```bash
# 验证JSON格式
python -m json.tool config/ai_adapters.json

# 恢复默认配置
cp config/ai_adapters.json.template config/ai_adapters.json

# 手动修复JSON
# 使用在线JSON验证器检查格式
```

## 🔐 权限问题

### 文件权限错误
**症状**: `PermissionError`
**解决方案**:
```bash
# Windows
icacls data /grant Everyone:F /T

# Linux/Mac
chmod -R 755 data/
chown -R $USER:$USER data/
```

### API权限不足
**症状**: API调用被拒绝
**解决方案**:
1. 检查API密钥权限范围
2. 验证账户余额和配额
3. 确认API服务可用性

## 🔧 日志和调试

### 启用详细日志
```python
# 修改日志级别
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用调试模式
python main.py --debug --verbose
```

### 查看系统日志
```bash
# Windows事件日志
eventvwr.msc

# Linux系统日志
tail -f /var/log/syslog

# 应用程序日志
tail -f logs/xiaoyi.log
```

## 🆘 获取支持

### 收集诊断信息
```bash
# 生成诊断报告
python -c "
import sys, platform
print(f'Python: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Architecture: {platform.architecture()}')
"

# 收集错误日志
grep -i error logs/*.log > error_report.txt
```

### 联系支持
1. **GitHub Issues**: 提交详细的问题报告
2. **QQ交流群**: 实时技术支持
3. **邮箱**: 2477194503@qq.com
4. **技术博客**: [依の技术栈](https://xun.eynet.top/)

### 问题报告模板
```markdown
## 问题描述
简要描述遇到的问题

## 系统环境
- 操作系统: Windows 11
- Python版本: 3.13
- 项目版本: 3.0 Demo

## 复现步骤
1. 第一步...
2. 第二步...
3. 第三步...

## 预期结果
描述预期的正常行为

## 实际结果
描述实际发生的情况

## 错误日志
```
粘贴相关的错误日志
```

## 其他信息
任何其他相关信息
```

## 🔄 维护建议

### 定期维护
```bash
# 每周清理日志
find logs/ -name "*.log" -mtime +7 -delete

# 每月备份配置
tar -czf backup_$(date +%Y%m%d).tar.gz config/ data/

# 更新依赖
pip list --outdated
pip install --upgrade package_name
```

### 监控脚本
```python
# health_check.py
import psutil
import json

def health_check():
    status = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }
    
    if status["memory_percent"] > 80:
        print("WARNING: High memory usage")
    
    return status

if __name__ == "__main__":
    print(json.dumps(health_check(), indent=2))
```