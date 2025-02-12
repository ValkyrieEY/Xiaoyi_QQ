# Command-Based Plugin Example

This document presents an example of a command-based plugin, detailing how to implement commands and handle user input.

## Overview

A command-based plugin allows users to interact with the bot by sending specific commands. This example will demonstrate how to create a simple command plugin that responds to user commands.

## Plugin Structure

The basic structure of a command plugin includes:

- **Command Registration**: Define the commands that the plugin will handle.
- **Command Handling**: Implement the logic to process the commands and generate responses.

## Example Code

Here is an example of a simple command plugin:

```python
from Hyper import Listener, Manager, Segments

@Listener.reg
async def command_handler(event: Events.Event, actions: Listener.Actions) -> None:
    user_message = str(event.message)

    if user_message.startswith("!hello"):
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text("Hello! How can I assist you today?")))

    elif user_message.startswith("!help"):
        help_message = "Available commands:\n!hello - Greet the bot\n!help - List available commands"
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(help_message)))
```

## Explanation

1. **Command Registration**: The `@Listener.reg` decorator registers the `command_handler` function to listen for events.
2. **Command Handling**: The function checks the user's message for specific commands (e.g., `!hello` and `!help`) and responds accordingly.

## Conclusion

This example demonstrates the basic implementation of a command-based plugin. You can expand upon this structure by adding more commands and enhancing the command handling logic to create a more interactive experience for users.