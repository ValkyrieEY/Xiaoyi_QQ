# File: /plugin-docs/plugin-docs/docs/api/actions.md

# Actions API Documentation

## Overview

The Actions API provides a set of functions that plugins can use to perform various actions within the platform. This includes sending messages, modifying group settings, and interacting with users.

## Available Actions

### Sending Messages

Plugins can send messages to users or groups using the following method:

```python
await actions.send(group_id, message)
```

- **group_id**: The ID of the group where the message will be sent.
- **message**: The message content, which can be a string or a message segment.

### Modifying Group Settings

Plugins can modify group settings using the following methods:

#### Setting Group Name

```python
await actions.set_group_name(group_id, new_name)
```

- **group_id**: The ID of the group whose name will be changed.
- **new_name**: The new name for the group.

#### Setting Group Announcement

```python
await actions.set_group_announcement(group_id, announcement)
```

- **group_id**: The ID of the group where the announcement will be set.
- **announcement**: The announcement text.

### Managing Group Members

Plugins can manage group members with the following actions:

#### Kicking a Member

```python
await actions.set_group_kick(group_id, user_id)
```

- **group_id**: The ID of the group from which the user will be kicked.
- **user_id**: The ID of the user to be kicked.

#### Banning a Member

```python
await actions.set_group_ban(group_id, user_id, duration)
```

- **group_id**: The ID of the group where the user will be banned.
- **user_id**: The ID of the user to be banned.
- **duration**: The duration of the ban in seconds.

## Conclusion

The Actions API is essential for creating interactive and responsive plugins. By utilizing these actions, developers can enhance user experience and manage group dynamics effectively.