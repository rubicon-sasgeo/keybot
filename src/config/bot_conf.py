import json

MOUSE_LEFT_PREFIX = '{MOUSE_LEFT'
MOUSE_DOUBLE_LEFT_PREFIX = '{MOUSE_DOUBLE_LEFT'
MOUSE_RIGHT_PREFIX = '{MOUSE_RIGHT'
MOUSE_DOUBLE_RIGHT_PREFIX = '{MOUSE_DOUBLE_RIGHT'
MOUSE_MOVE_REFIX = '{MOUSE_MOVE'
MOUSE_SCROLL_REFIX = '{MOUSE_SCROLL'


def is_mouse_left_click(keys: str) -> bool:
    line = keys.strip().casefold()
    return line.find(MOUSE_LEFT_PREFIX.casefold()) == 0


def is_mouse_double_left_click(keys: str) -> bool:
    line = keys.strip().casefold()
    return line.find(MOUSE_DOUBLE_LEFT_PREFIX.casefold()) == 0


def is_mouse_right_click(keys: str) -> bool:
    line = keys.strip().casefold()
    return line.find(MOUSE_RIGHT_PREFIX.casefold()) == 0


def is_mouse_double_right_click(keys: str) -> bool:
    line = keys.strip().casefold()
    return line.find(MOUSE_DOUBLE_RIGHT_PREFIX.casefold()) == 0


def is_mouse_move(keys: str) -> bool:
    line = keys.strip().casefold()
    return line.find(MOUSE_MOVE_REFIX.casefold()) == 0


def is_mouse_detected(keys: str):
    line = keys.strip().casefold()
    if(not is_mouse_left_click(keys)
       and not is_mouse_double_left_click(keys)
       and not is_mouse_right_click(keys)
       and not is_mouse_double_right_click(keys)
       and not is_mouse_move(keys)):
        return None

    coords = line[line.find('}') + 1:].split(',')
    if(len(coords) < 2):
        return None

    return list(map(int, coords))
