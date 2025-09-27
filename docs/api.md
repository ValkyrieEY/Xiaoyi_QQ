# 🔗 API文档

## 📋 API概述

小依QQ提供了丰富的API接口，支持自定义插件开发和外部服务集成。

## 🌐 RESTful API

### 基础信息
- **Base URL**: `http://localhost:8000/api`
- **认证方式**: Bearer Token
- **请求格式**: JSON
- **响应格式**: JSON

### 认证
```bash
# 获取访问令牌
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_password"
  }'
```

## 🤖 机器人API

### 发送消息
```http
POST /api/bot/send_message
Authorization: Bearer {token}
Content-Type: application/json

{
  "target_type": "group",
  "target_id": "123456",
  "message_type": "text",
  "content": "Hello World!"
}
```

### 获取群组列表
```http
GET /api/bot/groups
Authorization: Bearer {token}
```

响应：
```json
{
  "code": 200,
  "data": [
    {
      "group_id": "123456",
      "group_name": "测试群组",
      "member_count": 50
    }
  ]
}
```

### 获取用户信息
```http
GET /api/bot/user/{user_id}
Authorization: Bearer {token}
```

## 🧠 AI API

### 处理AI请求
```http
POST /api/ai/process
Authorization: Bearer {token}
Content-Type: application/json

{
  "adapter": "deepseek",
  "message": "你好，请介绍一下自己",
  "user_id": "123456",
  "context": {
    "group_id": "789012"
  }
}
```

### 切换AI模型
```http
POST /api/ai/switch
Authorization: Bearer {token}
Content-Type: application/json

{
  "user_id": "123456",
  "adapter": "gemini"
}
```

### 获取AI状态
```http
GET /api/ai/status
Authorization: Bearer {token}
```

响应：
```json
{
  "code": 200,
  "data": {
    "available_adapters": ["deepseek", "gemini", "chatgpt"],
    "default_adapter": "deepseek",
    "active_sessions": 5
  }
}
```

## 🔄 工作流API

### 创建工作流
```http
POST /api/workflow/create
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "自动回复",
  "description": "自动回复用户消息",
  "trigger": {
    "type": "message",
    "conditions": {
      "content_regex": "你好"
    }
  },
  "actions": [
    {
      "type": "send_message",
      "content": "你好！我是小依机器人"
    }
  ]
}
```

### 执行工作流
```http
POST /api/workflow/execute/{workflow_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "context": {
    "user_id": "123456",
    "group_id": "789012",
    "message": "你好"
  }
}
```

### 获取工作流列表
```http
GET /api/workflow/list
Authorization: Bearer {token}
```

## 🔌 插件API

### 安装插件
```http
POST /api/plugin/install
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
  "file": "plugin.zip",
  "auto_enable": true
}
```

### 启用/禁用插件
```http
POST /api/plugin/{plugin_name}/toggle
Authorization: Bearer {token}
Content-Type: application/json

{
  "enabled": true
}
```

### 获取插件列表
```http
GET /api/plugin/list
Authorization: Bearer {token}
```

响应：
```json
{
  "code": 200,
  "data": [
    {
      "name": "HelloWorld",
      "version": "1.0.0",
      "enabled": true,
      "description": "示例插件"
    }
  ]
}
```

## 📊 数据API

### 获取用户数据
```http
GET /api/data/user/{user_id}
Authorization: Bearer {token}
```

### 更新用户数据
```http
PUT /api/data/user/{user_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "points": 100,
  "level": 5,
  "last_checkin": "2024-01-01T12:00:00Z"
}
```

### 获取群组统计
```http
GET /api/data/group/{group_id}/stats
Authorization: Bearer {token}
```

## 🔔 事件API

### 注册事件监听
```http
POST /api/event/subscribe
Authorization: Bearer {token}
Content-Type: application/json

{
  "event_type": "message",
  "callback_url": "https://your-server.com/webhook",
  "filters": {
    "group_ids": ["123456"]
  }
}
```

### Webhook回调格式
```json
{
  "event_type": "message",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "user_id": "123456",
    "group_id": "789012",
    "message": "Hello",
    "message_type": "text"
  }
}
```

## 🛠️ 系统API

### 获取系统状态
```http
GET /api/system/status
Authorization: Bearer {token}
```

响应：
```json
{
  "code": 200,
  "data": {
    "status": "running",
    "uptime": 3600,
    "memory_usage": "45%",
    "cpu_usage": "12%",
    "active_connections": 10
  }
}
```

### 重启服务
```http
POST /api/system/restart
Authorization: Bearer {token}
```

### 获取日志
```http
GET /api/system/logs?level=error&limit=100
Authorization: Bearer {token}
```

## 📝 错误处理

### 错误响应格式
```json
{
  "code": 400,
  "message": "Bad Request",
  "error": "Invalid parameter",
  "details": {
    "field": "user_id",
    "reason": "User ID must be a number"
  }
}
```

### 常见错误码
- `200` - 成功
- `400` - 请求参数错误
- `401` - 未授权访问
- `403` - 权限不足
- `404` - 资源不存在
- `429` - 请求频率过高
- `500` - 服务器内部错误

## 🔐 安全考虑

### API密钥管理
```http
# 在请求头中包含API密钥
Authorization: Bearer your_api_key_here

# 或者在查询参数中包含
GET /api/endpoint?api_key=your_api_key_here
```

### 请求限制
- **频率限制**: 每分钟最多100个请求
- **大小限制**: 请求体最大10MB
- **超时设置**: 30秒请求超时

## 📚 SDK示例

### Python SDK
```python
import requests

class XiaoyiAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def send_message(self, target_type, target_id, content):
        data = {
            "target_type": target_type,
            "target_id": target_id,
            "message_type": "text",
            "content": content
        }
        response = requests.post(
            f"{self.base_url}/bot/send_message",
            json=data,
            headers=self.headers
        )
        return response.json()

# 使用示例
api = XiaoyiAPI("http://localhost:8000/api", "your_token")
result = api.send_message("group", "123456", "Hello!")
```

### JavaScript SDK
```javascript
class XiaoyiAPI {
    constructor(baseUrl, token) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
    
    async sendMessage(targetType, targetId, content) {
        const response = await fetch(`${this.baseUrl}/bot/send_message`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify({
                target_type: targetType,
                target_id: targetId,
                message_type: 'text',
                content: content
            })
        });
        return await response.json();
    }
}

// 使用示例
const api = new XiaoyiAPI('http://localhost:8000/api', 'your_token');
api.sendMessage('group', '123456', 'Hello!').then(console.log);
```

## 🧪 API测试

### Postman集合
提供完整的Postman API测试集合，包含所有端点的示例请求。

### 测试脚本
```bash
# 健康检查
curl http://localhost:8000/api/health

# 获取API版本
curl http://localhost:8000/api/version

# 测试认证
curl -H "Authorization: Bearer your_token" \
     http://localhost:8000/api/bot/groups
```

## 📖 更多资源

- [API变更日志](./api-changelog.md)
- [SDK下载](./sdk/)
- [示例代码](./examples/)
- [API测试工具](./tools/)