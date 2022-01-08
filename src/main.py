import config
from bots import KeySeq

conf = config.conf.get_config()
bot_file_name = config.conf.get_bot_file_name()

key_seq = KeySeq.KeySeq.from_json_file(bot_file_name)
if key_seq is None:
    print(f"Cannot find bot file {bot_file_name}. Failed to launch keybot.")
    exit(-1)

print(f"Bot [{key_seq.botname}] is active.")
print(f"Initial waiting for {key_seq.init_wait_ms} ms...")
KeySeq.KeySeq.wait_for_ms(key_seq.init_wait_ms)
key_seq.send_keys()
