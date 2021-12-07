import sys


def exist_param(key: str) -> bool:
    for i in range(len(sys.argv)):
        if(sys.argv[i].casefold() == key):
            return True

    return False


def get_param_value(key: str) -> str:
    for i in range(len(sys.argv)):
        if(sys.argv[i].casefold() == key):
            if(i < len(sys.argv) - 1):
                return sys.argv[i + 1]
            else:
                return ''

    return None


def sync_from_cmd_params(config) -> None:
    bot_folder = get_param_value('--bot_folder')
    if bot_folder is not None:
        config['default']['bot_folder'] = bot_folder

    bot_file_name = get_param_value('--bot_file_name')
    if bot_file_name is not None:
        config['default']['bot_file_name'] = bot_file_name

    interval_ms = get_param_value('--interval_ms')
    if interval_ms is not None:
        config['default']['interval_ms'] = interval_ms
