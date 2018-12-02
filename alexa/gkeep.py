import gkeepapi
from config import *

LISTS = {'grocery': GROCERY_LIST_ID}


def find_list_by_title(keep, txt):
    notes = keep.find(func=lambda x: x.title == txt)
    return notes

def login():
    keep = gkeepapi.Keep()
    success = keep.login(UN, PW)

    if success:
        return keep
    else:
        return None

def grocery_list(keep):
    l = keep.get(GROCERY_LIST_ID)
    return [x.text for x in l.items if not x.checked]

def add2grocery(keep, desc):
    l = keep.get(GROCERY_LIST_ID)
    l.add(desc)
    keep.sync()

# note = keep.createNote('Todo', 'Eat breakfast')
# note.pinned = True
# note.color = gkeepapi.node.ColorValue.Red
#
# keep.sync()

