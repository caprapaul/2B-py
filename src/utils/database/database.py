from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from utils.database.database_user import DatabaseUser
from utils.database.database_mute import DatabaseMute
from datetime import  datetime
import config
import logging

_logger = logging.getLogger(__name__)
_client: MongoClient = MongoClient(config.mongodb_uri)
_db: Database = _client[config.mongodb_database]

# region Users collection functions


def add_new_user(uid: int):
    """
    Adds a new user to the database.
    @param uid: int - The unique identifier of the user.
    @return: -
    """

    try:
        users: Collection = _db[config.mongodb_users]
        user_data = DatabaseUser(uid, 0, 0, 1, 0).to_dictionary()
        users.insert_one(user_data)
        _logger.info(f"User {uid} successfully added to the database.")

    except Exception as e:
        _logger.error(f"Error when trying to add user {uid} to the database : {e}")


def delete_user(uid: int):
    try:
        users: Collection = _db[config.mongodb_users]
        users.delete_one({'uid': uid})
        _logger.info(f"User {uid} successfully removed from the database.")

    except Exception as e:
        _logger.error(f"Error when trying to remove user {uid} from the database : {e}")


def get_user(uid: int):
    """
    Returns a database user.
    @param uid: int - The unique identifier of the user.
    @return: user: DatabaseUser
    """

    try:
        users: Collection = _db[config.mongodb_users]
        user = DatabaseUser.from_dictionary(users.find_one({'uid': uid}))

        return user

    except Exception as e:
        _logger.error(f"Error when trying to remove user {uid} from the database : {e}")


def get_user_xp_rank(uid: int):
    """
    Returns the xp rank of a user.
    @param uid: int - The unique identifier of the user.
    @return: rank: int
    """

    try:
        users: Collection = _db[config.mongodb_users]
        xp = get_user(uid).xp
        rank = users.count_documents({'exp': {'$gt': xp}}) + 1

        return rank

    except Exception as e:
        _logger.error(f"Error when trying to get the xp rank of user {uid} : {e}")


def get_user_karma_rank(uid: int):
    """
    Returns the karma rank of a user.
    @param uid: int - The unique identifier of the user.
    @return: rank: int
    """

    try:
        users: Collection = _db[config.mongodb_users]
        karma = get_user(uid).karma
        rank = users.count_documents({'karma': {'$gt': karma}}) + 1

        return rank

    except Exception as e:
        _logger.error(f"Error when trying to get the karma rank of user {uid} : {e}")


def get_top_level(start_index: int, count: int):
    """
    Returns the first 'count' users sorted by xp starting from 'start_index'.
    If there's not enough users, the list will be filled with DatabaseUser(0, 0, 0, 0 ,0).
    @param start_index: int - The index to start from. Cannot be higher than the users count.
    @param count: int - The amount of users to return.
    @return: top_users: list of DatabaseUser
    """

    try:
        users: Collection = _db[config.mongodb_users]

        assert start_index < users.estimated_document_count()

        user_docs = users.find().sort('exp', -1).skip(start_index - 1).limit(count)
        top_users = []

        for user_doc in user_docs:
            user = DatabaseUser.from_dictionary(user_doc)
            top_users.append(user)

        while len(top_users) < count:
            top_users.append(DatabaseUser())

        return top_users

    except Exception as e:
        _logger.error(f"Error when trying to get the top {count} users by xp starting from {start_index}: {e}")


def get_top_karma(start_index: int, count: int):
    """
    Returns the first 'count' users sorted by karma starting from 'start_index'.
    If there's not enough users, the list will be filled with DatabaseUser(0, 0, 0, 0 ,0).
    @param start_index: int - The index to start from. Cannot be higher than the users count.
    @param count: int - The amount of users to return.
    @return: top_users: list of DatabaseUser
    """

    try:
        users: Collection = _db[config.mongodb_users]

        assert start_index < users.estimated_document_count()

        user_docs = users.find().sort('karma', -1).skip(start_index - 1).limit(count)
        top_users = []

        for user_doc in user_docs:
            user = DatabaseUser.from_dictionary(user_doc)
            top_users.append(user)

        while len(top_users) < count:
            top_users.append(DatabaseUser())

        return top_users

    except Exception as e:
        _logger.error(f"Error when trying to get the top {count} users by karma starting from {start_index}: {e}")


def update_user(uid: int, user: DatabaseUser):
    """
   Checks if a user exists in the database.
   @param uid: int - The unique identifier of the user.
   @param user: DatabaseUser - The updated data of the user.
   @return: _: str
   """

    try:
        users: Collection = _db[config.mongodb_users]
        users.update_one({'uid': uid}, {'$set': user.to_dictionary()})

    except Exception as e:
        _logger.error(f"Error when trying to update user {uid} : {e}")


def user_exists(uid: int):
    """
    Checks if a user exists in the database.
    @param uid: int - The unique identifier of the user.
    @return: True if user exists False otherwise.
    """

    try:
        users: Collection = _db[config.mongodb_users]
        return users.count_documents({'uid': uid}) != 0

    except Exception as e:
        _logger.error(f"Error when trying to retrieve user {uid} from the database : {e}")


def _clear_users():
    try:
        users: Collection = _db[config.mongodb_users]
        users.delete_many({})
        _logger.info('Successfully cleared the users collection.')

    except Exception as e:
        _logger.error(f"Error when trying to clear users collection : {e}")

# endregion

# region Mutes collection functions


def add_mute(uid: int, expiration_date: datetime):
    """
    Adds a new mute to the database.
    @param uid: int - The unique identifier of the muted user.
    @param expiration_date: datetime - The expiration date
    @return: -
    """

    try:
        mutes: Collection = _db[config.mongodb_mutes]
        mute_data = DatabaseMute(uid, expiration_date.replace(microsecond=0)).to_dictionary()
        mutes.insert_one(mute_data)
        _logger.info(f"Mute {uid}: {str(expiration_date)} successfully added to the database.")

    except Exception as e:
        _logger.error(f"Error when trying to add mute {uid}: {str(expiration_date)} to the database : {e}")


def delete_mute(uid: int):
    """
    Removes a mute from the database.
    @param uid: int - The unique identifier of the muted user.
    @return: -
    """

    try:
        mutes: Collection = _db[config.mongodb_mutes]
        mutes.delete_one({'uid': uid})
        _logger.info(f"Mute {uid} successfully removed from the database.")

    except Exception as e:
        _logger.error(f"Error when trying to remove mute {uid} from the database : {e}")


def get_mutes():
    """
    Retrieves all mutes from the database.
    @return: all_mutes: list of DatabaseMute
    """

    try:
        mutes: Collection = _db[config.mongodb_mutes]
        mute_docs = mutes.find()

        all_mutes = []

        for mute_doc in mute_docs:
            all_mutes.append(DatabaseMute.from_dictionary(mute_doc))

        return all_mutes

    except Exception as e:
        _logger.error(f"Error when trying to get all mutes from the database : {e}")


def mute_exists(uid: int):
    """
    Check if a user is muted.
    @param uid: int - The unique identifier of the user.
    @return: True if user exists False otherwise.
    """

    try:
        mutes: Collection = _db[config.mongodb_mutes]
        return mutes.count_documents({'uid': uid}) != 0

    except Exception as e:
        _logger.error(f"Error when trying to check if mute {uid} exists : {e}")
        
        
def _clear_mutes():
    try:
        mutes: Collection = _db[config.mongodb_mutes]
        mutes.delete_many({})
        _logger.info('Successfully cleared the mutes collection.')

    except Exception as e:
        _logger.error(f"Error when trying to clear mutes collection : {e}")

# endregion
