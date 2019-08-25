# This is an example for your bot's configuration file.
# Please fill out everything that is necessary and rename the file to `config.py`.


# ---------------------- CORE ----------------------
# These is the core config your bot will need at any time.

# This is your bot's token. Not your Client Secret or the Client ID, remember that!
# KEEP THIS PRIVATE AT ANY TIME!
token = ''

# The bot's prefix.
prefix = '!'

# A brief description about your bot.
description = 'A bot.'

# The ID of the bot's owner.
owner_id = 123456

# The initial extensions that will be loaded when the bot starts. Specify the directory where to search for the extensions.
cog_dir = 'cogs'   # Only change this if you want to load cogs from another directory.

# ------------------- MONGODB -------------------
# This is the configuration your bot needs to connect to a MongoDB database.

# Your MongoDB credentials.
mongodb_user = ''
mongodb_password = ''
mongodb_database = 'database'
mongodb_uri = f'mongodb://{mongodb_user}:{mongodb_password}@localhost:27017/{mongodb_database}'

# The database collection that stores all users
mongodb_users = 'users'

# The database collection that stores all mutes
mongodb_mutes = 'mutes'

# The database collection used for unit tests
mongodb_test = 'test'
