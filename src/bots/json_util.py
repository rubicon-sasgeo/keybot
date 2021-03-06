import json
import KeySeq


def _json_object_hook(d):
    return KeySeq('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)
