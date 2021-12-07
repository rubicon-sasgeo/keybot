import os
import toml

import config.cmd_line as cmd_line

CONF = None


def get_config():
    global CONF
    if CONF is not None:
        return CONF

    file_name = os.path.join(os.path.abspath(os.curdir), 'config.toml')
    CONF = toml.load(file_name)

    cmd_line.sync_from_cmd_params(CONF)
    return CONF


def get_bot_file_name():
    config = get_config()
    folder_name = config['default']['bot_folder']
    if not os.path.isdir(folder_name):
        folder_name = os.path.join(os.path.abspath(os.curdir), folder_name)

    return os.path.join(os.path.abspath(
        folder_name), config['default']['bot_file_name'])
