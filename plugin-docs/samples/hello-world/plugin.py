# This is a simple "Hello World" plugin example.

from Hyper import Listener, Manager, Segments

@Listener.reg
async def on_message(event: Events.GroupMessageEvent, actions: Listener.Actions) -> None:
    user_message = str(event.message)

    if "hello" in user_message.lower():
        response = "Hello, world! 🌍"
        await actions.send(group_id=event.group_id, message=Manager.Message(Segments.Text(response)))