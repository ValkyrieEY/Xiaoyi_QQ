# plugin-template.py

class Plugin:
    def __init__(self):
        self.name = "Your Plugin Name"
        self.version = "0.1.0"
        self.description = "A brief description of your plugin."

    async def on_message(self, event, actions):
        """
        Handle incoming messages.
        :param event: The event object containing message details.
        :param actions: The actions object to perform actions like sending messages.
        """
        user_message = str(event.message)
        # Add your message handling logic here

        # Example response
        if user_message == "hello":
            await actions.send(group_id=event.group_id, message="Hello, world!")

    async def on_event(self, event, actions):
        """
        Handle specific events.
        :param event: The event object containing event details.
        :param actions: The actions object to perform actions.
        """
        # Add your event handling logic here