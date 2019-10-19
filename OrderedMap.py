from RedBlackTreeMap import RedBlackTreeMap


class OrderedMap(object):
    def __init__(self):
        self.map = RedBlackTreeMap()

    def remove(self, key):
        self.map.remove(key)

    def __getitem__(self, key):
        return self.map.get(key)

    def __setitem__(self, key, val):
        self.map.insert(key, val)

    def __contains__(self, key):
        return self.map.contains(key)

    def __delitem__(self, key):
        self.remove(key)

    def __len__(self):
        return len(self.map)

    def __iter__(self):
        return self.map.__iter__()

    def __str__(self):
        if len(self.map) == 0:
            return '{}'

        res = []
        for (key, val) in self.map:
            res.append('%s: %s' % (str(key), str(val)))

        return "{%s}" % ", ".join(res)
