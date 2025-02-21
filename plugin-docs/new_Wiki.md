创建新的插件
为了简儿原生功能的丰富性，提升开发者二次开发的便捷性，简儿于 2025.02 推出了全新的 NEXT PREVIEW 分支。此分支的原生功能实际是 2.0 版本的迭代，但是本分支新增了插件兼容性，为广大开发者们提供了更友好的插件开发入口。本文将引导你如何快速、顺利地开发 简儿（NEXT PREVIEW 分支） 的插件并投入使用。

Important

NEXT PREVIEW 分支是预览分支，插件兼容性有待评估，投入实际使用可能不会具有预期中的稳定性。请谨慎使用本分支产品，如有遇到Bug，请立即反馈于 Issue ，感谢您的谅解与支持。

0. 原理讲解（必看）
你可以在简儿的根目录一下找到 plugins 文件夹，这是插件的存放目录。

插件可以以以下形式在 plugins 文件夹中存在：

.py 文件
.pyw 文件
文件夹
其中 .py 文件和 .pyw 文件是以单个文件形式存在的单个插件，可以直接放在 plugins 文件夹根目录下。文件夹形式存在的插件是由多个文件组合形成的单个插件，文件夹中必须包含入口文件 setup.py ，文件夹直接放在 plugins 文件夹根目录下。文件夹形式存在的插件，其内部的子文件夹不会被识别为插件。

setup.py 和其他以单个文件形式存在的单个插件具有与相同的内容规范，将会在后文 1. 开始制作 中详细讲解。

无论任何形式的插件，当其文件名以 d_ 开头时，如 d_something.py ，将会被忽略加载，即为 已禁用插件 。你可以很方便地在群里发送 “启用插件” 或 “禁用插件” 来使简儿加载或忽略加载某些插件。你可以发送 “重载插件” 来使简儿重新从磁盘中加载全部插件，而无需重启简儿。你还可以发送 “插件视角” 来查看插件的运行报告，哪些插件是否已被启用，或因为何种原因加载失败。

1. 开始制作
创建单个文件形式存在的插件
在 plugins 文件夹 下，新建 .py 文件，文件名会作为插件名称。如 Hello World.py

创建文件夹形式存在的插件
在 plugins 文件夹 下，新建文件夹，文件夹名称会作为插件名称。如 Hello World

在该文件夹下，新建 setup.py 文件，该文件会作为插件的入口文件，响应插件的一系列事件。如果缺少该文件，则插件将会无法被正常加载。

接下来， setup.py 文件和单个文件形式存在的插件操作方法完全相同，开发者只需要按照接下来的步骤即可完成插件注册和插件编写。

注册插件
这是一个示例：一个 Hello World.py 插件具有以下代码

TRIGGHT_KEYWORD = "你好，世界"
HELP_MESSAGE = "仅仅就是一句 Hello world 🤔？"
async def on_message(event, actions, Manager, Segments):
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("Hello, world! 🌍")))
        return True
仅需5行代码即可完成开发一个可以发送消息的插件，可见简儿插件开发的高效性。接下来，本文将对代码进行讲解。

TRIGGHT_KEYWORD ：str 类型，插件的触发关键词，即当用户在群里发送的消息包含此关键词时，触发此插件。 在示例 Hello World.py 插件中，当用户发送 “你好，世界” 时，此插件将会被触发。（如图所示）
image

HELP_MESSAGE ：str 类型，插件的帮助消息。当用户在群里@简儿 或者发送 “帮助” 时，展示的帮助文件中会包括此帮助消息文本。（如图所示）
QQ_1739525797968

async def on_message() ：插件的入口函数，当插件被触发时，执行 on_message() 函数内部的代码。注意，此方法必须异步。

return True ：阻断执行后续功能，此行可选。当插件返回 True 时，简儿将停止执行后续的功能，防止多个具有相同触发关键词的功能一起被执行。

恭喜你，已经成功地新建并注册好了一个插件，现在这个插件可以被正常地加载和调用啦！下一步，本文将深入讲解如何实现更多丰富功能。

参数传入
async def on_message() 函数可以接受很多参数，各种各样的参数说明详见 Variables.md

直接将想要被传入的参数填写在函数的括号内即可，例如 async def on_message(event, actions, Manager, Segments)

实现插件
await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("Hello, world! 🌍")))
actions.send() ：发送一条内容

event.group_id ：获取发送消息的用户所在的群号码

Manager.Message ：一个消息内容

Segments.Text ：一段纯文本消息

恭喜你，你已经实现了自己的第一个插件！快去试试吧～

2. 拓展知识
永久触发插件
永久触发插件 是指无论用户发任何消息，该插件都会收到事件并被触发。

如果你想要做一个 永久触发插件 ，仅需将改动一个值

TRIGGHT_KEYWORD = "Any"
可以看到，示例的插件将 TRIGGHT_KEYWORD 设置为了 Any ，只要用户发送了新消息，插件每一次都会被立刻执行了