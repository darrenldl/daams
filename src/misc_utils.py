def collect_duplicates(l):
    s = set(l)
    ret = []
    for e in s:
        if l.count(e) > 1:
            ret.append(e)
    return ret
