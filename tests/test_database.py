import unittest
import utils.database.database as db
from datetime import datetime
import time
import config

_users_collection = config.mongodb_users


def set_test_collection():
    config.mongodb_users = config.mongodb_test


def reset_test_collection():
    config.mongodb_users = _users_collection


class TestDatabase(unittest.TestCase):
    def test_add_get_user(self):
        set_test_collection()
        db._clear_users()

        user_id = 123456

        self.assertFalse(db.user_exists(user_id))

        db.add_new_user(user_id)

        self.assertTrue(db.user_exists(user_id))

        user = db.get_user(user_id)

        self.assertEqual(user.uid, user_id)
        self.assertEqual(user.karma, 0)
        self.assertEqual(user.level, 1)
        self.assertEqual(user.xp, 0)
        self.assertEqual(user.udc, 0)

        db._clear_users()
        reset_test_collection()

    def test_delete_user(self):
        set_test_collection()
        db._clear_users()

        user_id = 123456

        db.add_new_user(user_id)

        db.delete_user(user_id)

        self.assertFalse(db.user_exists(user_id))

        db._clear_users()
        reset_test_collection()

    def test_update_user(self):
        set_test_collection()
        db._clear_users()

        user_id = 123456

        db.add_new_user(user_id)

        user = db.get_user(user_id)
        user.karma = 1
        db.update_user(user_id, user)

        user = db.get_user(user_id)
        self.assertEqual(user.karma, 1)

        db._clear_users()
        reset_test_collection()

    def test_get_ranks(self):
        set_test_collection()
        db._clear_users()

        user_id_karma = 123456
        user_id_xp = 654321

        db.add_new_user(user_id_karma)
        db.add_new_user(user_id_xp)

        user_karma = db.get_user(user_id_karma)
        user_karma.karma = 1
        db.update_user(user_id_karma, user_karma)

        user_xp = db.get_user(user_id_xp)
        user_xp.xp = 1
        db.update_user(user_id_xp, user_xp)

        self.assertEqual(db.get_user_xp_rank(user_id_xp), 1)
        self.assertEqual(db.get_user_xp_rank(user_id_karma), 2)

        self.assertEqual(db.get_user_karma_rank(user_id_xp), 2)
        self.assertEqual(db.get_user_karma_rank(user_id_karma), 1)

        db._clear_users()
        reset_test_collection()

    def test_get_top(self):
        set_test_collection()
        db._clear_users()

        user_id_karma = 123456
        user_id_xp = 654321

        db.add_new_user(user_id_karma)
        db.add_new_user(user_id_xp)

        user_karma = db.get_user(user_id_karma)
        user_karma.karma = 1
        db.update_user(user_id_karma, user_karma)

        user_xp = db.get_user(user_id_xp)
        user_xp.xp = 1
        db.update_user(user_id_xp, user_xp)

        top_level = db.get_top_level(1, 10)
        self.assertEqual(top_level[0].uid, user_id_xp)
        self.assertEqual(top_level[2].uid, 0)

        top_karma = db.get_top_karma(1, 10)
        self.assertEqual(top_karma[0].uid, user_id_karma)
        self.assertEqual(top_karma[2].uid, 0)

        db._clear_users()
        reset_test_collection()

    def test_add_get_mute(self):
        set_test_collection()
        db._clear_mutes()

        user_id = 123456

        self.assertFalse(db.mute_exists(user_id))

        expiration = datetime.now().replace(microsecond=0)

        db.add_mute(user_id, expiration)

        self.assertTrue(db.mute_exists(user_id))

        mute = db.get_mutes()[0]

        self.assertEqual(mute.uid, user_id)
        self.assertEqual(mute.expiration_date, expiration)

        db._clear_mutes()
        reset_test_collection()

    def test_delete_mute(self):
        set_test_collection()
        db._clear_mutes()

        user_id = 123456
        expiration = datetime.now().replace(microsecond=0)

        db.add_mute(user_id, expiration)

        db.delete_mute(user_id)

        self.assertFalse(db.mute_exists(user_id))

        db._clear_mutes()
        reset_test_collection()


if __name__ == '__main__':
    unittest.main()
