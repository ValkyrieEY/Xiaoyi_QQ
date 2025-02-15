# CustomAPI 插件文档

## 插件信息
- 名称：CustomAPI
- 版本：1.0.0
- 作者：XiaoyiAPI

## 功能简介
CustomAPI 是一个灵活的 API 调用插件，允许用户通过 Web 界面配置和管理自定义 API 接口。插件支持文本和图片类型的响应，并能够处理多种参数类型。

## 变量支持
- JSON数据提取：【json#路径】
- 用户信息：【发送者QQ】【发送者昵称】【at】
- 消息内容：【用户消息】
- 时间信息：【当前时间】
- 格式化：【换行】
- 参数值：【参数#参数名】
- 媒体：【图片链接】

## 配置说明
### 配置文件位置
配置文件默认保存在插件目录下的 `custom_api_config.json` 中。

### 配置格式
```json
{
  "apis": [
    {
      "command": "天气",
      "url": "https://api.example.com/weather",
      "response_type": "text",
      "response_path": "weather.text",
      "params": [
        {
          "name": "city",
          "type": "user_input",
          "value": ""
        }
      ]
    }
  ]
}
```

### 配置项说明
- `command`: 触发命令
- `url`: API 接口地址
- `response_type`: 响应类型（支持 text/image）
- `response_path`: JSON 响应数据的提取路径
- `params`: API 参数配置
  - `name`: 参数名称
  - `type`: 参数类型
    - `user_input`: 用户输入
    - `text`: 固定文本
    - `sender_id`: 发送者ID
  - `value`: 固定文本值（仅在 type 为 text 时使用）

## 使用方法
### 配置界面
1. 发送 `/api config` 命令打开配置界面
2. 浏览器会自动打开 `http://localhost:4997`
3. 在 Web 界面中配置 API 参数

### API 调用
直接发送配置好的命令即可，例如：
```
天气 北京
```

## 注意事项
1. 确保配置的 API 接口可以正常访问
2. response_path 配置正确，以便准确提取所需数据
3. Web 配置界面端口默认为 4997

## 错误处理
插件会对各种异常情况进行处理：
- 配置文件读取失败时会使用默认配置
- API 请求失败时会返回错误信息
- 数据提取失败时会返回原始响应

## 依赖项
- Flask
- requests
- Hyper 框架
