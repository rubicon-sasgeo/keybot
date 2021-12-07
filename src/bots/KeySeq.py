import os
from dataclasses import dataclass
import json
import ctypes
from time import sleep
from colorama import (Fore, Style)
import config


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
            print(Fore.GREEN + f'========== Bot Starts ==========')

        MessageBox = ctypes.windll.user32.MessageBoxW
        qty = self.loop if self.must_loop() else 0
        for i in range(qty):
            print(Fore.BLUE + f'--- Round #{i} ---')
            for j in range(len(self.keys)):
                MessageBox(None, self.keys[j], self.window_name, 0)
                if logging:
                    print(Fore.GREEN + f'sent [{self.keys[j]}]...')
                if self.interval_ms > 0:
                    if logging:
                        print(Fore.GREEN +
                              f'-- sleeping for {self.interval_ms} ms...')
                    sleep(float(self.interval_ms) / 1000.0)
            print('\r\n')

        if logging:
            print(Fore.GREEN + f'========== Bot Ends ==========')
        pass
