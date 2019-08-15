from pymongo import MongoClient
import config
import urllib.parse
import logging

_logger = logging.getLogger(__name__)
_client = MongoClient(config.mongodb_uri)
_db = _client[config.mongodb_database]


def _get_user_attribute(uid: int, attribute: str):
    try:
        return _db.users[uid][attribute]
    except Exception as e:
        _logger.error(f"Error when trying to get attribute {attribute} from user {uid} : {e}")
