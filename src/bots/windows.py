from typing import List
import pywinauto
from pywinauto import mouse

from config import bot_conf
from bots import KeySeq


def sendkeys(window_name: str, lines: List[str], interval_ms: int, logging: bool):
    window_list = pywinauto.Desktop(backend="uia").windows()
    for w in window_list:
        # print(w.window_text())
        if (w.window_text().casefold().find(window_name.casefold()) >= 0):
            w.set_focus()
            for keys in lines:
                mouse_loc = bot_conf.is_mouse_detected(keys)
                if mouse_loc is None:
                    pywinauto.keyboard.send_keys(keys)
                else:
                    for i in range(0, len(mouse_loc), 2):
                        if(bot_conf.is_mouse_left_click(keys)):
                            mouse.click(button='left', coords=(
                                mouse_loc[i], mouse_loc[i+1]))
                        elif(bot_conf.is_mouse_double_left_click(keys)):
                            mouse.double_click(button='left', coords=(
                                mouse_loc[i], mouse_loc[i+1]))
                        elif(bot_conf.is_mouse_right_click(keys)):
                            mouse.click(button='right', coords=(
                                mouse_loc[i], mouse_loc[i+1]))
                        elif(bot_conf.is_mouse_right_click(keys)):
                            mouse.double_click(button='right', coords=(
                                mouse_loc[i], mouse_loc[i+1]))
                        elif(bot_conf.is_mouse_move(keys)):
                            mouse.move(coords=(mouse_loc[i], mouse_loc[i+1]))
                            # mouse.scroll()
                        if logging:
                            print(
                                f'-- mouse {keys} --')

                if interval_ms > 0:
                    if logging:
                        print(f'-- line sleeping for {interval_ms} ms...')
                    KeySeq.KeySeq.wait_for_ms(interval_ms)
            break
