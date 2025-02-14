# AntiSpam 插件

一个用于 Hyper 框架的 QQ 群聊反刷屏插件。

## 功能特点

- 自动检测群内刷屏行为
- 可配置的时间窗口和消息数量阈值
- 记录并跟踪用户警告次数
- 支持管理员配置和权限系统
- 完整的命令系统

## 安装

1. 将插件文件放置在你的 Hyper 插件目录中
2. 确保配置文件目录有写入权限
3. 重启 Hyper 框架

## 配置文件示例

### antispam_config.json
```json
{
  "check_time": 15,        
  "max_messages": 8,       
  "enabled": true,         
  "warn_records": {
    "12345678": {         
      "count": 2,         
      "last_warn_time": "2025-02-14 12:30:45"
    },
    "87654321": {
      "count": 1,
      "last_warn_time": "2025-02-14 13:15:20"
    }
  }
}
```

### xiaoyi_admins.json
```json
{
  "admins": ["123456789", "987654321"],
  "enabled": true,
  "system_enabled": true
}
```

## 命令列表

所有命令需要管理员权限：

```
!as status          - 查看系统状态
!as set check_time <秒数> - 设置检测时间窗口
!as set max_messages <数量> - 设置最大消息数
!as toggle         - 开关系统
!as clear <QQ号>    - 清除指定用户的警告记录
!as help           - 显示帮助信息
```

## 默认配置

- 检测时间窗口：10秒
- 最大消息数：10条
- 系统默认开启

## 警告系统

当检测到刷屏行为时，会发送如下格式的警告：

```
⚠️ 刷屏警告
用户：用户名 (QQ号)
XX秒内发送了XX条消息
这是第X次警告
上次警告时间：YYYY-MM-DD HH:MM:SS
```

## 使用示例

### 修改检测时间
```
!as set check_time 15
```

### 修改最大消息数
```
!as set max_messages 8
```

### 查看系统状态
```
!as status
```

## 依赖

- Python 3.6+
- Hyper 框架

## 关于

- 作者：Xiaoyi
- 版本：1.0.0
- 许可证：保留所有权利

## 贡献

欢迎提交 Issue 和 Pull Request。

## 常见问题

1. 配置文件无法创建？
   - 请确保插件目录具有写入权限

2. 命令无响应？
   - 检查是否已添加管理员QQ号
   - 确认命令格式是否正确

3. 警告消息未发送？
   - 检查机器人是否具有群发言权限
   - 确认系统已启用(!as status 查看)