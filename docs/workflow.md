# 🔄 工作流自动化

## 📋 工作流概述

工作流系统是小依机器人的核心功能之一，允许用户通过可视化界面创建、管理和执行自动化工作流。工作流基于路由规则和执行步骤的组合，实现智能的消息处理和自动化操作。

## 🎯 核心特性

### 🎪 可视化管理
- **直观界面**: 通过WebUI进行可视化配置和管理
- **拖拽排序**: 支持步骤的拖拽式重新排序
- **实时预览**: 实时查看工作流配置效果
- **测试功能**: 内置测试运行功能，验证工作流逻辑

### 🎯 路由规则系统
支持多种触发条件：
- **关键词匹配**: 消息包含特定关键词时触发
- **正则表达式**: 使用正则表达式匹配复杂模式
- **用户权限**: 根据用户权限级别触发（ADMIN、USER等）
- **群组过滤**: 特定群组中的消息触发
- **用户过滤**: 特定用户的消息触发
- **自定义条件**: 支持复杂的条件逻辑判断

### 🔧 执行步骤类型
- **调用插件**: 执行现有插件功能
- **发送消息**: 向用户或群组发送文本消息
- **条件判断**: 基于变量或上下文进行分支处理
- **设置变量**: 设置和管理工作流变量
- **延迟执行**: 添加时间延迟控制
- **停止工作流**: 中断工作流执行

## 📂 配置结构

### 主配置文件
```json
// config/workflow_config.json
{
  "enabled": true,
  "max_execution_time": 60,
  "log_level": "info",
  "default_priority": 100,
  "concurrent_workflows": 10,
  "auto_reload": true,
  "debug_mode": false
}
```

### 工作流定义结构
```json
// config/workflows/example_workflow.json
{
  "id": "wf_example_welcome",
  "name": "自动欢迎新成员",
  "description": "当有新成员加入群聊时，自动发送欢迎消息",
  "enabled": true,
  "created_at": "2025-01-16T10:00:00",
  "updated_at": "2025-01-16T10:00:00",
  "routes": [
    {
      "id": "route_new_member",
      "name": "新成员加入检测",
      "rule_type": "keyword",
      "condition": "欢迎",
      "priority": 100,
      "enabled": true,
      "description": "检测新成员加入事件"
    }
  ],
  "steps": [
    {
      "id": "step_welcome_message",
      "name": "发送欢迎消息",
      "type": "message",
      "enabled": true,
      "description": "向新成员发送欢迎消息",
      "config": {
        "message": "欢迎 ${user_name} 加入我们的大家庭！请仔细阅读群规，有问题可以咨询管理员。",
        "reply": false
      }
    }
  ]
}
```

## 🎮 工作流类型

### 1. 关键词触发工作流
```json
{
  "id": "wf_keyword_response",
  "name": "关键词自动回复",
  "description": "检测到特定关键词后自动回复",
  "enabled": true,
  "routes": [
    {
      "id": "route_help",
      "name": "帮助关键词检测",
      "rule_type": "keyword",
      "condition": "帮助",
      "priority": 100,
      "enabled": true
    }
  ],
  "steps": [
    {
      "id": "step_help_response",
      "name": "发送帮助信息",
      "type": "message",
      "enabled": true,
      "config": {
        "message": "🔥 小依机器人帮助\n\n可用命令：\n- 签到\n- AI聊天\n- 工作流管理\n\n更多功能请参考文档。",
        "reply": true
      }
    }
  ]
}
```

### 2. 正则表达式工作流
```json
{
  "id": "wf_regex_filter",
  "name": "正则匹配过滤",
  "description": "使用正则表达式过滤特定消息格式",
  "enabled": true,
  "routes": [
    {
      "id": "route_qq_number",
      "name": "QQ号码检测",
      "rule_type": "regex",
      "condition": "[1-9]\\d{4,10}",
      "priority": 90,
      "enabled": true
    }
  ],
  "steps": [
    {
      "id": "step_qq_warning",
      "name": "发送警告",
      "type": "message",
      "enabled": true,
      "config": {
        "message": "⚠️ 检测到QQ号码，请注意保护个人隐私！",
        "reply": true
      }
    }
  ]
}
```

### 3. 权限检查工作流
```json
{
  "id": "wf_admin_tools",
  "name": "管理员工具",
  "description": "只有管理员才能使用的功能",
  "enabled": true,
  "routes": [
    {
      "id": "route_admin_check",
      "name": "管理员权限检查",
      "rule_type": "user_permission",
      "condition": "ADMIN",
      "priority": 200,
      "enabled": true
    }
  ],
  "steps": [
    {
      "id": "step_permission_check",
      "name": "权限验证",
      "type": "condition",
      "enabled": true,
      "config": {
        "condition": "'ADMIN' in ${user_permissions}",
        "true_steps": ["step_admin_action"],
        "false_steps": ["step_deny_action"]
      }
    },
    {
      "id": "step_admin_action",
      "name": "执行管理操作",
      "type": "plugin",
      "enabled": true,
      "config": {
        "plugin_name": "AdminTools",
        "parameters": {}
      }
    },
    {
      "id": "step_deny_action",
      "name": "拒绝访问",
      "type": "message",
      "enabled": true,
      "config": {
        "message": "⛔ 权限不足，只有管理员才能使用此功能。",
        "reply": true
      }
    }
  ]
}
```

## 🔧 高级功能

### 条件分支处理
```json
{
  "id": "step_condition_example",
  "name": "条件判断示例",
  "type": "condition",
  "enabled": true,
  "config": {
    "condition": "${user_level} >= 10",
    "true_steps": ["step_vip_welcome"],
    "false_steps": ["step_normal_welcome"]
  }
},
{
  "id": "step_vip_welcome",
  "name": "VIP用户欢迎",
  "type": "message",
  "enabled": true,
  "config": {
    "message": "🎆 欢迎VIP用户 ${user_name}！您享有特殊权益。",
    "reply": false
  }
},
{
  "id": "step_normal_welcome",
  "name": "普通用户欢迎",
  "type": "message",
  "enabled": true,
  "config": {
    "message": "👋 欢迎新用户 ${user_name}！",
    "reply": false
  }
}
```

### 插件集成
```json
{
  "id": "step_plugin_call",
  "name": "调用签到插件",
  "type": "plugin",
  "enabled": true,
  "config": {
    "plugin_name": "CheckIn",
    "parameters": {
      "user_id": "${user_id}",
      "group_id": "${group_id}"
    },
    "save_result": true,
    "result_variable": "checkin_result"
  }
}
```

### 变量操作
```json
{
  "id": "step_set_variable",
  "name": "设置用户积分",
  "type": "variable",
  "enabled": true,
  "config": {
    "variable_name": "user_points",
    "variable_value": "${checkin_result.points}",
    "scope": "workflow"
  }
}
```

### 延迟执行
```json
{
  "id": "step_delay",
  "name": "等待2秒",
  "type": "delay",
  "enabled": true,
  "config": {
    "duration": 2,
    "unit": "seconds"
  }
}
```

## 📝 变量系统

工作流支持强大的变量系统，可以在步骤间传递数据：

### 内置变量
- `${message}` - 触发消息内容
- `${user_id}` - 发送者QQ号
- `${user_name}` - 发送者昵称
- `${group_id}` - 群组ID
- `${group_name}` - 群组名称
- `${user_permissions}` - 用户权限列表
- `${current_time}` - 当前时间
- `${bot_name}` - 机器人名称

### 自定义变量
使用“设置变量”步骤创建自定义变量：
```json
{
  "type": "variable",
  "config": {
    "variable_name": "welcome_count",
    "variable_value": "${welcome_count + 1}",
    "scope": "global"
  }
}
```

### 变量作用域
- `workflow` - 工作流级别，仅在当前工作流中有效
- `global` - 全局级别，所有工作流共享
- `user` - 用户级别，针对特定用户的变量

## 🎪 使用方法

### 1. 打开工作流管理界面

在小依配置助手中，点击“工作流管理”选项卡进入工作流管理界面。

```bash
# 启动WebUI管理界面
python launcher.py
# 或者直接访问
http://localhost:5007
```

### 2. 创建新工作流

1. 点击“新建”按钮
2. 输入工作流名称和描述
3. 设置工作流的启用状态
4. 配置工作流ID和基本信息

### 3. 配置路由规则

在“路由规则”标签页中：
1. 点击“添加路由”按钮
2. 选择路由类型：
   - `keyword` - 关键词匹配
   - `regex` - 正则表达式
   - `user_permission` - 用户权限
   - `group_filter` - 群组过滤
   - `user_filter` - 用户过滤
3. 输入匹配条件
4. 设置优先级（数字越大优先级越高）
5. 保存路由规则

### 4. 添加执行步骤

在“执行步骤”标签页中：
1. 点击“添加步骤”按钮
2. 选择步骤类型：
   - `message` - 发送消息
   - `plugin` - 调用插件
   - `condition` - 条件判断
   - `variable` - 设置变量
   - `delay` - 延迟执行
   - `stop` - 停止工作流
3. 配置步骤参数
4. 使用“上移”/“下移”按钮调整步骤顺序

### 5. 测试工作流

在“测试运行”标签页中：
1. 输入测试消息
2. 选择模拟的用户和群组
3. 点击“开始测试”
4. 查看测试结果和执行日志

## 📊 性能优化

### 并发执行优化
```json
// config/workflow_config.json
{
  "concurrent_workflows": 10,    // 最大并发数
  "max_execution_time": 60,      // 最大执行时间
  "auto_reload": true            // 自动重载配置
}
```

### 路由优先级优化
- 将常用的路由设置更高的优先级
- 避免过于复杂的正则表达式
- 合理分组相关的路由规则

### 步骤优化
- 避免过多的条件嵌套
- 合理使用变量缓存
- 限制单个工作流的步骤数量（建议不超过20个）

## 🗺️ 文件结构

```
config/
├── workflow_config.json         # 主配置文件
└── workflows/                   # 工作流定义目录
    ├── README.md                # 使用说明
    ├── wf_example_welcome.json  # 示例：欢迎新成员
    ├── wf_auto_moderation.json  # 示例：自动审核
    ├── wf_smart_qa.json         # 示例：智能问答
    ├── wf_admin_tools.json      # 示例：管理工具
    └── wf_daily_tasks.json      # 示例：每日任务
```

## 🛠️ 故障排除

### 常见问题

#### 工作流不触发
1. **检查路由规则**
   - 确认关键词匹配正确
   - 检查正则表达式语法
   - 验证权限设置

2. **确认工作流已启用**
   ```json
   {
     "enabled": true,  // 工作流必须启用
     "routes": [
       {
         "enabled": true  // 路由也必须启用
       }
     ]
   }
   ```

3. **查看执行日志**
   - 检查系统日志输出
   - 启用调试模式：`"debug_mode": true`

#### 步骤执行失败
1. **检查步骤配置**
   ```json
   {
     "type": "plugin",
     "config": {
       "plugin_name": "CheckIn",    // 确认插件名称正确
       "parameters": {}             // 检查参数格式
     }
   }
   ```

2. **验证变量引用**
   - 确认变量名拼写正确
   - 检查变量作用域
   - 使用测试功能验证

#### 变量无法识别
1. **检查变量语法**
   ```json
   {
     "message": "${user_name} 你好！"  // 正确格式
   }
   ```

2. **验证变量存在**
   - 使用测试功能查看可用变量
   - 检查变量作用域设置

### 调试技巧

1. **启用调试模式**
   ```json
   // config/workflow_config.json
   {
     "debug_mode": true,
     "log_level": "debug"
   }
   ```

2. **使用测试功能**
   - 在WebUI中逐步测试工作流
   - 查看每个步骤的执行结果
   - 验证变量值和传递

3. **日志分析**
   - 查看系统日志中的工作流执行信息
   - 关注错误和警告信息
   - 分析执行时间和性能瓶颈

## 🔗 相关资源

- [工作流系统详细说明](../config/workflows/README.md)
- [示例工作流配置](../config/workflows/)
- [WebUI管理界面](../plugins/start_webui.py)
- [插件开发指南](./plugin-development.md)