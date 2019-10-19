from RedBlackTree import RedBlackTree


class OrderedSet(object):
    def __init__(self):
        self.bst = RedBlackTree()

    def add(self, key):
        self.bst.insert(key)

    def remove(self, key):
        self.bst.remove(key)

    def __contains__(self, key):
        return self.bst.contains(key)

    def __len__(self):
        return len(self.bst)

    def __iter__(self):
        return self.bst.__iter__()

    def __str__(self):
        if len(self.bst) == 0:
            return '[]'

        res = []
        for key in self.bst:
            res.append(str(key))

        return "[%s]" % ", ".join(res)
