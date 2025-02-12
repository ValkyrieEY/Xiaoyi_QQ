# Events API Documentation

## Overview

The Events API allows plugins to listen for and respond to various events that occur within the system. This enables developers to create interactive and responsive plugins that can react to user actions, system changes, and other triggers.

## Available Events

### 1. GroupMessageEvent

- **Description**: Triggered when a message is sent in a group.
- **Payload**: Contains information about the message, sender, and group.
- **Usage**: Use this event to respond to messages from users in a group.

### 2. PrivateMessageEvent

- **Description**: Triggered when a private message is received.
- **Payload**: Contains information about the sender and the message content.
- **Usage**: Use this event to handle direct messages from users.

### 3. GroupMemberIncreaseEvent

- **Description**: Triggered when a new member joins a group.
- **Payload**: Contains information about the new member and the group.
- **Usage**: Use this event to welcome new members or perform setup tasks.

### 4. GroupMemberDecreaseEvent

- **Description**: Triggered when a member leaves a group.
- **Payload**: Contains information about the departing member and the group.
- **Usage**: Use this event to handle member departures, such as sending farewell messages.

### 5. GroupAddInviteEvent

- **Description**: Triggered when a user is invited to join a group.
- **Payload**: Contains information about the invitee and the group.
- **Usage**: Use this event to automatically approve invites based on certain criteria.

## Listening for Events

To listen for events in your plugin, you can use the following syntax:

```python
@Listener.reg
async def handler(event: Events.Event, actions: Listener.Actions) -> None:
    if isinstance(event, Events.GroupMessageEvent):
        # Handle group message event
        pass
```

## Best Practices

- Always check the type of the event before processing it to avoid errors.
- Use asynchronous functions to handle events to ensure non-blocking behavior.
- Log important events for debugging and monitoring purposes.

## Conclusion

The Events API is a powerful tool for creating dynamic plugins that can interact with users and respond to changes in the environment. By understanding and utilizing the available events, developers can enhance the functionality and user experience of their plugins.