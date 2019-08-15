import logging
import sys
import os
from datetime import datetime
from pathlib import Path

import click

from core.bot import Bot


@click.group(invoke_without_command=True)
@click.option('--stream-log', is_flag=True, help='Adds a stderr stream handler to the bot\'s logging component.')
def root(stream_log):
    bot = Bot()

    logging.getLogger('discord').setLevel(logging.INFO)

    log_dir = Path(os.path.dirname(__file__)).parent / 'logs'
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        filename=f'../logs/2b-py.{datetime.now().strftime("%d%m%y-%H%M%S")}.log',
        encoding='utf-8',
        mode='w'
    )

    formatter = logging.Formatter('[{levelname}] ({asctime}) - {name}:{lineno} - {message}', '%Y-%m-%d %H:%M:%S',
                                  style='{')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if stream_log:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    try:
        bot.run()
    except KeyboardInterrupt:
        bot.loop.create_task(bot.logout())


if __name__ == '__main__':
    sys.exit(root())
