import datetime
from enum import Enum


class Status(Enum):
    online = 'online'
    offline = 'offline'
    idle = 'idle'
    dnd = 'dnd'
    do_not_disturb = 'dnd'
    invisible = 'invisible'

    def __str__(self):
        return self.value


class TestMember:
    def __init__(self, name: str, uid: int, discriminator: str, avatar: str, avatar_url: str,
                 bot: bool, status: Status, joined_at: datetime.datetime):
        self.joined_at = joined_at
        self.status = status
        self.bot = bot
        self.avatar_url = avatar_url
        self.avatar = avatar
        self.name = name
        self.id = uid
        self.discriminator = discriminator
