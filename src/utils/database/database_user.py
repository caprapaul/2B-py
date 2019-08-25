class DatabaseUser:
    def __init__(self, uid: int = 0, karma: int = 0, xp: int = 0, level: int = 0, udc: int = 0):
        self.uid = uid
        self.karma = karma
        self.xp = xp
        self.level = level
        self.udc = udc

    def to_dictionary(self):
        data = {
            'uid': self.uid,
            'karma': self.karma,
            'exp': self.xp,
            'level': self.level,
            'udc': self.udc
        }
        return data

    @staticmethod
    def from_dictionary(data):
        user = DatabaseUser()

        user.uid = data['uid']
        user.karma = data['karma']
        user.xp = data['exp']
        user.udc = data['udc']
        user.level = data['level']

        return user
