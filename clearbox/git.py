
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
        return d[sha], sha
    else:
        return None, sha


def get_branch():
    """
    Returns tuple of current branch name and a boolean whether there are
    uncommitted changes.
    """
    txt = os.popen(f'git status -s -b').read().strip()
    m = re.search('## (.*)\s', txt)
    branch = m.group(1)

    m = re.search('M (.*)\s', txt)
    if m is None:
        mods = False
    else:
        mods = True
    return branch, mods


def get_datetime():
    datestr = os.popen('git show -s --format=%ci').read().strip()
    return datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S %z').astimezone(pytz.utc)


def get_status_string():
    #branch, mods = get_branch()
    #mods = "Modified" if mods else ''
    #datestr = get_datetime()
    txt = os.popen('git log --format="%H \'%ci\' %d" -n 1').read().strip()
    m = re.search("(?P<sha>[0-9a-f]+) '(?P<datestr>[ 0-9\-:\+]+)'\s+\((?P<refname>.*)\)", txt)
    sha = m.group('sha')
    date = datetime.datetime.strptime(m.group('datestr'), '%Y-%m-%d %H:%M:%S %z').astimezone(pytz.utc)
    datestr = date.strftime('%Y-%m-%d %H:%M')
    refname = m.group('refname')
    # refname:
    # HEAD, tag: ver0
    # HEAD
    # HEAD -> master, tag: ver1

    m = re.search('HEAD -> (?P<branch>.+?)($|,)', refname)
    branch = m.group('branch') if m is not None else ''

    m = re.search('tag: (?P<tag>.+?)($|,)', refname)
    tag = m.group('tag') if m is not None else ''

    return f"{tag} {branch} {sha[:7]} {datestr}"

if __name__ == '__main__':
    print(get_sha())
    print(get_datetime())
