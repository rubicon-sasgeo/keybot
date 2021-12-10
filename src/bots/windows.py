from typing import List
import pywinauto


def sendkeys(window_name: str, lines: List[str]):
    window_list = pywinauto.Desktop(backend="uia").windows()
    for w in window_list:
        # print(w.window_text())
        if (w.window_text().casefold().find(window_name.casefold()) >= 0):
            w.set_focus()
            for keys in lines:
                pywinauto.keyboard.send_keys(keys)
            break
