import unittest
from utils.database import *
from utils.database import _clear_users
import datetime
from .test_member import TestMember, Status

_users_collection = config.mongodb_users


def set_test_collection():
    config.mongodb_users = config.mongodb_test


def reset_test_collection():
    config.mongodb_users = _users_collection


class TestDatabase(unittest.TestCase):
    def test_add_get_user(self):
        set_test_collection()
        _clear_users()

        now = datetime.datetime.now()
        self.test_user = TestMember('Test', 123456, '1234', 'avatar1234', 'avatar_url',
                                    False, Status.online, now)

        self.assertFalse(user_exists(123456))
        add_new_user(self.test_user)
        self.assertTrue(user_exists(123456))

        self.assertEqual(get_user_karma(123456), 0)
        self.assertEqual(get_user_join_date(123456), now.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(get_user_level(123456), 1)
        self.assertEqual(get_user_rank(123456), 0)
        self.assertEqual(get_user_xp(123456), 0)

        _clear_users()

        reset_test_collection()


if __name__ == '__main__':
    unittest.main()
