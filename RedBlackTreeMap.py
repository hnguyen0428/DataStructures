from RedBlackTree import RedBlackTree, RedBlackNode


class RedBlackNodeMap(RedBlackNode):
	def __init__(self, key, val):
		super(RedBlackNodeMap, self).__init__(key)
		self.val = val


class TreeMapIterator(object):
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
		res = (node.key, node.val)
		if node.right is not None and node.right is not self.sentinel:
			curr = node.right
			while curr is not None and curr is not self.sentinel:	# Add left
				self.stack.append(curr)
				curr = curr.left

		return res


class RedBlackTreeMap(RedBlackTree):
	def __init__(self):
		self.root = None
		self.numEle = 0
		self.sentinel = RedBlackNodeMap(0, 0)

	def insert(self, key, val):
		n = self.searchNode(key)
		if n:	# If key already exists, change the value and return
			n.val = val
			return

		newNode = RedBlackNodeMap(key, val)
		self.bstInsert(newNode)
		self.insertRepair(newNode)
		self.numEle += 1

	def get(self, key):
		n = self.searchNode(key)
		if n:
			return n.val
		else:
			raise KeyError(str(key))

	def printInorderHelper(self, root, keys):
		if root and root is not self.sentinel:
			self.printInorderHelper(root.left, keys)
			keys.append('%s: %s' % (str(root.key), str(root.val)))
			self.printInorderHelper(root.right, keys)

	def printInorder(self):
		keys = []
		self.printInorderHelper(self.root, keys)
		print("{%s}" % ", ".join(keys))

	def __iter__(self):
		return TreeMapIterator(self.root, self.sentinel)
