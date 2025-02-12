# quickstart.md

# 快速入门指南

欢迎来到插件开发的快速入门指南！本指南将帮助您快速创建第一个插件，并提供基本的设置和执行步骤。

## 1. 环境准备

在开始之前，请确保您已经完成了以下步骤：

- 安装 Python 3.7 或更高版本。
- 安装所需的依赖项（请参阅 [安装指南](installation.md)）。

## 2. 创建插件

1. **创建插件目录**  
   在您的项目中创建一个新的插件目录，例如 `my_first_plugin`。

2. **创建插件文件**  
   在插件目录中创建一个名为 `plugin.py` 的文件，并添加以下基本代码：

   ```python
   def on_message(event, actions):
       return "Hello, World!"
   ```

3. **插件结构**  
   确保您的插件目录结构如下：

   ```
   my_first_plugin/
   └── plugin.py
   ```

## 3. 加载插件

在主程序中，您需要加载新创建的插件。确保您的主程序包含以下代码：

```python
import importlib.util
import os
import sys

PLUGIN_FOLDER = "plugins"

def load_plugins():
    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(PLUGIN_FOLDER, filename))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

load_plugins()
```

## 4. 运行插件

确保您的主程序正在运行，并发送一条消息以测试插件。您应该会收到 "Hello, World!" 的响应。

## 5. 下一步

现在您已经成功创建并运行了第一个插件！接下来，您可以查看 [插件结构](plugin-structure.md) 文档，以了解更多关于插件组件的信息，或者参考 [创建插件](creating-plugins.md) 指南，深入学习插件开发的最佳实践。

祝您开发愉快！