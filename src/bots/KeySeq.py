import os
from dataclasses import dataclass
import json
from time import sleep
import random
import config
import bots.windows as windows


@dataclass
class KeySeq:
    botname = ""
    window_name = ""
    loop = -1
    keys = []
    init_wait_ms = (1000,)
    interval_ms = 100
    loop_interval_ms = 1000
    random_internval_ms = 0  # 0 or negative to disable

    def __init__(
        self,
        botname,
        window_name,
        loop,
        keys,
        init_wait_ms,
        interval_ms,
        loop_interval_ms,
        random_internval_ms,
    ) -> None:
        self.botname = botname
        self.window_name = window_name
        self.loop = int(loop)
        self.keys = keys
        self.init_wait_ms = int(init_wait_ms)
        self.interval_ms = int(interval_ms)
        self.loop_interval_ms = int(loop_interval_ms)
        self.random_internval_ms = int(random_internval_ms)
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

    def randomize_loop_interval(self) -> int:
        if self.random_internval_ms == 0:
            return self.loop_interval_ms

        additional = random.randrange(0, self.random_internval_ms, 1)
        if random.choice([0, 1]) == 0:
            interval = self.loop_interval_ms - additional
        else:
            interval = self.loop_interval_ms + additional

        if interval < 0:
            interval = 10000
        return interval

    def send_keys(self) -> None:
        conf = config.conf.get_config()
        logging = bool(conf["debug"]["logging"])
        if logging:
            print(f"========== Bot Initiated ==========")

        qty = self.loop if self.must_loop() else 0
        for i in range(qty):
            print(f"--- Round #{i} ---")
            (lines, wait_ms, index) = self.get_sub_seq(0)
            while lines is not None:
                windows.sendkeys(self.window_name, lines, self.interval_ms, logging)
                if logging:
                    print(f"sent [{lines}]...")
                    if wait_ms > 0:
                        print(f"wait for [{wait_ms}] ms...")
                        KeySeq.wait_for_ms(wait_ms)
                    else:
                        print(f"No wait specified...")

                (lines, wait_ms, index) = self.get_sub_seq(index)

            if self.loop_interval_ms > 0 and i + 1 < qty:
                wait_ms = self.randomize_loop_interval()
                if logging:
                    print(f"-- loop sleeping for {wait_ms} ms...")
                KeySeq.wait_for_ms(wait_ms)
            print("\r\n")

        if logging:
            print(f"========== Bot Dissolved ==========")
        pass

    def get_sub_seq(self, index: int):
        if index >= len(self.keys):
            return (None, None, None)

        lines = []
        wait_ms = 0
        for index in range(index, len(self.keys)):
            if type(self.keys[index]) == int:
                wait_ms = int(self.keys[index])
                break
            lines.append(self.keys[index])

        return (lines, wait_ms, index + 1)

    @classmethod
    def wait_for_ms(cls, duration_ms) -> None:
        sleep(float(duration_ms) / 1000.0)
