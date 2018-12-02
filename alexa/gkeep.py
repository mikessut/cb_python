import gkeepapi
from config import *


def find_list_by_title(keep, txt):
    notes = keep.find(func=lambda x: x.title == txt)
    return [(x.title, x.id) for x in notes]

def login():
    keep = gkeepapi.Keep()
    success = keep.login(UN, PW)

    if success:
        return keep
    else:
        return None

def read_list(keep, list_id):
    l = keep.get(list_id)
    return [x.text for x in l.items if not x.checked]


def add_to_list(keep, list_id, desc):
    l = keep.get(list_id)
    l.add(desc)
    keep.sync()
