from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import config
import logging

_logger = logging.getLogger(__name__)
_client: MongoClient = MongoClient(config.mongodb_uri)
_db: Database = _client[config.mongodb_database]

# region Public functions


def add_new_user(user):
    """
    Adds a new user to the database.
    @param user: discord.Member - User to add.
    @return: -
    """

    try:
        users: Collection = _db[config.mongodb_users]
        user_data = {
            'username': user.name,
            'userid': user.id,
            'discriminator': user.discriminator,
            'avatar': user.avatar,
            'avatarURL': user.avatar_url,
            'bot': 1 if user.bot else 0,
            'status': str(user.status),
            'joinDate': user.joined_at.strftime('%Y-%m-%d %H:%M:%S'),
            'karma': 0,
            'exp': 0,
            'level': 1,
            'rank': 0
        }
        users.insert_one(user_data)
        _logger.info(f"User {user.name}#{user.discriminator} successfully added to the database.")

    except Exception as e:
        _logger.error(f"Error when trying to add user {user.id} to the database : {e}")


def delete_user(uid: int):
    try:
        users: Collection = _db[config.mongodb_users]
        users.delete_one({'userid': uid})
        _logger.info(f"User {uid} successfully removed from the database.")

    except Exception as e:
        _logger.error(f"Error when trying to remove user {uid} from the database : {e}")


def get_user_xp(uid: int):
    """
    Returns the xp of a user.
    @param uid: int - The unique identifier of the user.
    @return: xp: int
    """

    reader = _get_user_attribute(uid, 'exp')

    xp = int(reader)
    return xp


def get_user_karma(uid: int):
    """
    Returns the karma of a user.
    @param uid: int - The unique identifier of the user.
    @return: karma: int
    """

    reader = _get_user_attribute(uid, 'karma')

    karma = int(reader)
    return karma


def get_user_rank(uid: int):
    """
    Returns the rank of a user.
    @param uid: int - The unique identifier of the user.
    @return: rank: int
    """

    reader = _get_user_attribute(uid, 'rank')

    rank = int(reader)
    return rank


def get_user_level(uid: int):
    """
    Returns the level of a user.
    @param uid: int - The unique identifier of the user.
    @return: level: int
    """

    reader = _get_user_attribute(uid, 'level')

    level = int(reader)
    return level


def get_user_join_date(uid: int):
    """
    Returns the join date of a user.
    @param uid: int - The unique identifier of the user.
    @return: _: str
    """

    return _get_user_attribute(uid, 'joinDate')


def add_user_xp(uid: int, amount: int):
    """
    Adds xp to a user.
    @param uid: int - The unique identifier of the user.
    @param amount: int - The amount of xp to add.
    @return: -
    """

    reader = _get_user_attribute(uid, 'exp')
    old_xp = int(reader)
    _update_user_attribute(uid, 'exp', old_xp + amount)


def add_user_level(uid: int, amount: int):
    """
    Adds level to a user.
    @param uid: int - The unique identifier of the user.
    @param amount: int - The amount of levels to add.
    @return: -
    """

    reader = _get_user_attribute(uid, 'level')
    old_level = int(reader)
    _update_user_attribute(uid, 'level', old_level + amount)


def add_user_karma(uid: int, amount: int):
    """
    Adds karma to a user.
    @param uid: int - The unique identifier of the user.
    @param amount: int - The amount of karma to add.
    @return: -
    """
    
    reader = _get_user_attribute(uid, 'karma')
    old_karma = int(reader)
    _update_user_attribute(uid, 'karma', old_karma + amount)


def user_exists(uid: int):
    """
    Checks if a user exists in the database.
    @param uid: int - The unique identifier of the user.
    @return: _: str
    """

    try:
        users: Collection = _db[config.mongodb_users]
        return users.count_documents({'userid': uid}) != 0

    except Exception as e:
        _logger.error(f"Error when trying to retrieve user {uid} from the database : {e}")

# endregion

# region Private functions


def _get_user_attribute(uid: int, attribute: str):
    try:
        users: Collection = _db[config.mongodb_users]
        user = users.find_one({'userid': uid})
        return user[attribute]

    except Exception as e:
        _logger.error(f"Error when trying to get attribute {attribute} from user {uid} : {e}")


def _update_user_attribute(uid: int, attribute: str, value):
    try:
        users: Collection = _db[config.mongodb_users]
        users.update_one({'userid': uid}, {'$set': {attribute: value}})

    except Exception as e:
        _logger.error(f"Error when trying to update attribute {attribute} from user {uid} with value {value} : {e}")


def _clear_users():
    try:
        users: Collection = _db[config.mongodb_users]
        users.delete_many({})

    except Exception as e:
        _logger.error(f"Error when trying to clear users collection : {e}")

# endregion
