# filepath: /plugin-docs/samples/command-handler/plugin.py

from Hyper import Listener, Events, Manager, Segments

@Listener.reg
async def command_handler(event: Events.Event, actions: Listener.Actions) -> None:
    if isinstance(event, Events.GroupMessageEvent):
        user_message = str(event.message)

        if user_message.startswith("!hello"):
            response = "Hello! How can I assist you today?"
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(response)))

        elif user_message.startswith("!help"):
            help_message = (
                "Available commands:\n"
                "!hello - Greet the bot\n"
                "!help - List available commands"
            )
            await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(help_message)))

        # Add more command handling logic here as needed