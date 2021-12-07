from colorama import (Fore, Style)
import config
from bots import KeySeq

conf = config.conf.get_config()
bot_file_name = config.conf.get_bot_file_name()

key_seq = KeySeq.KeySeq.from_json_file(bot_file_name)
if key_seq is None:
    print(
        Fore.RED + f'Cannot find bot file {bot_file_name}. Failed to launch keybot.')
    print(Style.RESET_ALL)
    exit(-1)

print(Fore.YELLOW + f'Bot [{key_seq.botname}] is active.')
print(Style.RESET_ALL)
key_seq.send_keys()
print(Style.RESET_ALL)
