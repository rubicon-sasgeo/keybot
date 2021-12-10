import os
from dataclasses import dataclass
import json
from time import sleep
import config
import bots.windows as windows


@dataclass
class KeySeq:
    botname = ''
    window_name = ''
    loop = -1
    keys = []
    interval_ms = 1000

    def __init__(self, botname, window_name, loop, keys, interval_ms) -> None:
        self.botname = botname
        self.window_name = window_name
        self.loop = int(loop)
        self.keys = keys
        self.interval_ms = int(interval_ms)
        pass

    def must_loop(self) -> bool:
        return self.loop > 0

    @classmethod
    def from_json(cls, json_text: str):
        param_list = json.loads(json_text)
        key_seq = cls(**param_list)
        return key_seq

    @classmethod
    def from_json_file(cls, json_file_name: str):
        if not os.path.isfile(json_file_name):
            return None

        with open(json_file_name) as file_ptr:
            key_seq = cls.from_json(file_ptr.read())
            # param_list = json.load(file_ptr)
            # key_seq = cls(**param_list)

            file_ptr.close()
            return key_seq

    def send_keys(self) -> None:
        conf = config.conf.get_config()
        logging = bool(conf['debug']['logging'])
        if logging:
            print(f'========== Bot Starts ==========')

        qty = self.loop if self.must_loop() else 0
        for i in range(qty):
            print(f'--- Round #{i} ---')
            (lines, wait_ms, index) = self.get_sub_seq(0)
            while(lines is not None):
                windows.sendkeys(self.window_name, lines)
                if logging:
                    print(f'sent [{lines}]...')
                    if(wait_ms > 0):
                        print(f'wait for [{wait_ms}] ms...')
                        sleep(wait_ms)
                    else:
                        print(f'No wait specified...')

                (lines, wait_ms, index) = self.get_sub_seq(index)

            if self.interval_ms > 0:
                if logging:
                    print(f'-- sleeping for {self.interval_ms} ms...')
                sleep(float(self.interval_ms) / 1000.0)
            print('\r\n')

        if logging:
            print(f'========== Bot Ends ==========')
        pass

    def get_sub_seq(self, index: int):
        if(index >= len(self.keys)):
            return (None, None, None)

        lines = []
        wait_ms = 0
        for index in range(index, len(self.keys)):
            if type(self.keys[index]) == int:
                wait_ms = int(self.keys[index])
                break
            lines.append(self.keys[index])

        return (lines, wait_ms, index + 1)
