# File: /plugin-docs/plugin-docs/docs/reference/plugin-manifest.md

# 插件清单文件

插件清单文件是每个插件的核心组成部分，包含了插件的基本信息和配置选项。以下是插件清单文件的结构及其各个字段的说明。

## 文件结构

```json
{
    "name": "插件名称",
    "version": "插件版本",
    "description": "插件描述",
    "author": "作者名称",
    "license": "许可证类型",
    "main": "主入口文件",
    "dependencies": {
        "依赖包名称": "版本号"
    },
    "config": {
        "配置项名称": "默认值"
    }
}
```

## 字段说明

- **name**: 插件的名称，应该是唯一的，便于识别。
- **version**: 插件的版本号，遵循语义化版本控制（SemVer）规范。
- **description**: 对插件功能的简短描述，帮助用户理解插件的用途。
- **author**: 插件的作者或维护者的名称。
- **license**: 插件的许可证类型，例如 MIT、GPL 等。
- **main**: 插件的主入口文件，通常是一个 Python 文件，负责初始化插件。
- **dependencies**: 插件所需的依赖包及其版本，确保插件在运行时能够找到所需的库。
- **config**: 插件的配置选项，允许用户根据需要自定义插件的行为。

## 示例

以下是一个插件清单文件的示例：

```json
{
    "name": "hello-world-plugin",
    "version": "1.0.0",
    "description": "一个简单的 Hello World 插件",
    "author": "张三",
    "license": "MIT",
    "main": "plugin.py",
    "dependencies": {
        "requests": "^2.25.1"
    },
    "config": {
        "greeting": "Hello, World!"
    }
}
```

## 注意事项

- 确保插件清单文件的 JSON 格式正确，避免语法错误。
- 在发布插件之前，更新版本号和描述，以反映最新的更改和功能。