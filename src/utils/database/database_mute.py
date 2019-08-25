from datetime import datetime


class DatabaseMute:
    def __init__(self, uid: int = 0, expiration_date: datetime = datetime.now()):
        self.uid = uid
        self.expiration_date = expiration_date

    def to_dictionary(self):
        data = {
            'uid': self.uid,
            'expiration_date': self.expiration_date
        }
        return data

    @staticmethod
    def from_dictionary(data):
        mute = DatabaseMute()

        mute.uid = data['uid']
        mute.expiration_date = data['expiration_date']

        return mute
