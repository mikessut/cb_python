

# from: http://code.activestate.com/recipes/577850-search-sequences-for-sub-sequence/

def _search(forward, source, target, start=0, end=None):
    """Naive search for sublist in list.

    Example:
    misc.search([4,5,1,2,5,6], [1,2])
      => 2
    """
    m = len(source)
    n = len(target)
    if end is None:
        end = m
    else:
        end = min(end, m)
    if n == 0 or (end-start) < n:
        # target is empty, or longer than source, so obviously can't be found.
        return None
    if forward:
        x = range(start, end-n+1)
    else:
        x = range(end-n, start-1, -1)
    for i in x:
        if source[i:i+n] == target:
            return i
    return None

import functools
searchsub = functools.partial(_search, True)
rsearchsub = functools.partial(_search, False)
