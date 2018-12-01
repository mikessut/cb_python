
import re
import os
import sys
import datetime
import pytz


def get_sha():
    # txt = os.popen('git branch -v').read()
    # m = re.search('\* (?P<branch>[^\s]+)\s(?P<sha>[^\s]+)', txt)
    # return(m.group('sha'))
    return os.popen('git rev-list HEAD -n 1').read().strip()


def get_tags():
    txt = os.popen('git tag').read().strip()
    return txt.splitlines()

def get_tag_sha(tag):
    sha = get_sha()
    tag_sha = os.popen(f'git rev-list {tag} -n 1').read().strip()
    return tag_sha


def get_tag():

    d = {}
    for tag in get_tags():
        sha = get_tag_sha(tag)
        d[sha] = tag

    sha = get_sha()
    if sha in d.keys():
        return d[sha]
    else:
        return None


def get_datetime():
    datestr = os.popen('git show -s --format=%ci').read().strip()
    return datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S %z').astimezone(pytz.utc)

if __name__ == '__main__':
    print(get_sha())
    print(get_datetime())
