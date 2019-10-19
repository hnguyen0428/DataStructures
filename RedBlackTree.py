class RedBlackNode(object):
    def __init__(self, key):
        self.key = key
        self.red = False
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        p = self.parent
        if p:
            return p.parent

        return None

class TreeIterator(object):
    def __init__(self, root, sentinel):
        self.itr = root
        self.sentinel = sentinel
        self.stack = []
        curr = root
        while curr is not None and curr is not sentinel:
            self.stack.append(curr)
            curr = curr.left

    def __iter__(self):
        return self

    def next(self):
        if len(self.stack) == 0:
            raise StopIteration

        node = self.stack.pop()
        res = node.key
        if node.right is not None and node.right is not self.sentinel:
            curr = node.right
            while curr is not None and curr is not self.sentinel:   # Add left
                self.stack.append(curr)
                curr = curr.left

        return res


    def __next__(self):
        return self.next()

class RedBlackTree(object):
    def __init__(self):
        self.root = None
        self.numEle = 0
        self.sentinel = RedBlackNode(0)

    def rotateLeft(self, x):
        y = x.right
        x.right = y.left    # y's left subtree becomes x's right subtree

        if y.left is not self.sentinel: # y has a left child
            y.left.parent = x

        y.parent = x.parent
        if x.parent is self.sentinel:
            self.root = y
        elif x is x.parent.left:    # x was left child of its parent
            x.parent.left = y
        else:                       # x was right child of its parent
            x.parent.right = y

        y.left = x
        x.parent = y

    def rotateRight(self, x):
        y = x.left
        x.left = y.right    # y's right subtree becomes x's left subtree

        if y.right is not self.sentinel:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is self.sentinel:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.right = x
        x.parent = y

    def bstInsert(self, z):
        itr = self.root
        y = self.sentinel
        while itr is not None and itr is not self.sentinel:
            y = itr
            if z.key < itr.key:
                itr = itr.left
            else:
                itr = itr.right

        z.parent = y
        if y is self.sentinel:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        z.red = True
        z.left = self.sentinel
        z.right = self.sentinel

    def insertRepair(self, z):
        # z's parent is red, cannot happen -> must fix
        while z.parent.red:
            gp = z.grandparent()
            if gp is not None:
                if z.parent is gp.left: # z's parent is left child
                    y = gp.right    # Uncle of z
                    # Case 1: when the color of z's uncle is red, we must change
                    # both the uncle and the parent of z to black and change
                    # grandparent to red in order to prevent violation of the
                    # tree properties.
                    if y.red:
                        z.parent.red = False
                        y.red = False
                        gp.red = True
                        z = gp
                    else:
                        # Case 2: when color of z's uncle is black, and z is the
                        # right child of its parent. z must be rotated up to its
                        # parent's spot. This transforms the situation into case 3.
                        if z is z.parent.right:
                            z = z.parent
                            self.rotateLeft(z)

                        # Case 3: when color of z's uncle is black, and z is the
                        # left child of its parent. Grandparent must be rotated right
                        z.parent.red = False
                        gp = z.grandparent()
                        gp.red = True
                        self.rotateRight(gp)
                else:   # z's parent is right child
                    y = gp.left     # Uncle of z
                    # Case 1
                    if y.red:
                        z.parent.red = False
                        y.red = False
                        gp.red = True
                        z = gp
                    # Case 2
                    else:
                        if z is z.parent.left:
                            z = z.parent
                            self.rotateRight(z)

                        z.parent.red = False
                        gp = z.grandparent()
                        gp.red = True
                        self.rotateLeft(gp)

        self.root.red = False

    def insert(self, key):
        n = self.searchNode(key)
        if n:   # If key already exists, do nothing
            return

        newNode = RedBlackNode(key)
        self.bstInsert(newNode)
        self.insertRepair(newNode)
        self.numEle += 1

    # Replace the deleted node u with v while maintaining bst structure
    def transplant(self, u, v):
        if u.parent is self.sentinel:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def searchMin(self, node):
        while node.left and node.left is not self.sentinel:
            node = node.left
        return node

    def searchNode(self, key):
        curr = self.root
        while curr is not None and curr is not self.sentinel:
            if key == curr.key:
                return curr
            elif key > curr.key:    # Key larger, move right
                curr = curr.right
            else:                   # Key smaller, move left
                curr = curr.left

        return None

    # Delete node z
    def removeNode(self, z):
        y = z
        ogColor = y.red
        if z.left is self.sentinel:
            x = z.right
            self.transplant(z, z.right)
        elif z.right is self.sentinel:
            x = z.left
            self.transplant(z, z.left)
        # The node being removed has both children, must look for the minimum
        # of the right subtree of this node
        else:
            y = self.searchMin(z.right)
            ogColor = y.red
            x = y.right
            if y.parent is z:   # y's parent is the node getting deleted
                # That means x should point to y, since y will be taking the spot
                # of z
                x.parent = y
            else:
                # y is getting deleted from its spot and moved up to where z is
                # so it has to be deleted from its original spot => must transplant
                # with right child
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            # Transplant z and y since z is getting deleted
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.red = z.red

        # x's parent points to the node that is in the place of the node that
        # got deleted
        if not ogColor:
            self.removeRepair(x)

    def removeRepair(self, x):
        while x is not self.root and not x.red:
            if x is x.parent.left:  # x is left child
                w = x.parent.right
                # Case 1: x's sibling w is red (and x is not), in which case
                # w has to be set to black. x's parent color is set to red.
                if w.red:
                    w.red = False
                    x.parent.red = True
                    self.rotateLeft(x.parent)
                    w = x.parent.right
                # Case 2: x's sibling w has both black children (meaning w can be red)
                if not w.left.red and not w.right.red:
                    w.red = True
                    x = x.parent
                # Case 3: x's sibling w has red left child and black right child
                # We can swap color of w and its left child and then rotate right
                # without violating any properties (since w is red and gets rotated
                # into its right child's position, which is already red)
                else:
                    if not w.right.red:
                        w.left.red = False

                        w.red = True
                        self.rotateRight(w)
                        w = x.parent.right

                    # Case 4: x's sibling w has left black child and red right child
                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False

                    self.rotateLeft(x.parent)
                    x = self.root

            else:   # x is right child
                w = x.parent.left
                # Case 1:
                if w.red:
                    w.red = False
                    x.parent.red = True
                    self.rotateRight(x.parent)
                    w = x.parent.left
                # Case 2:
                if not w.left.red and not w.right.red:
                    w.red = True
                    x = x.parent
                else:
                    if not w.left.red:
                        w.right.red = False

                        w.red = True
                        self.rotateLeft(w)
                        w = x.parent.left

                    w.red = x.parent.red
                    x.parent.red = False
                    w.left.red = False

                    self.rotateRight(x.parent)
                    x = self.root

        x.red = False

    def remove(self, key):
        n = self.searchNode(key)
        if n is None:
            raise KeyError(str(key))

        self.removeNode(n)
        self.numEle -= 1

    def contains(self, key):
        n = self.searchNode(key)
        return n is not None

    def printInorderHelper(self, root, keys):
        if root and root is not self.sentinel:
            self.printInorderHelper(root.left, keys)
            keys.append(str(root.key))
            self.printInorderHelper(root.right, keys)

    def printInorder(self):
        keys = []
        self.printInorderHelper(self.root, keys)
        print("[%s]" % ", ".join(keys))

    def __len__(self):
        return self.numEle

    def __iter__(self):
        return TreeIterator(self.root, self.sentinel)
