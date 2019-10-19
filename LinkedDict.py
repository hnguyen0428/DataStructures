class ListNode(object):
	def __init__(self, key, val):
		self.key = key
		self.val = val
		self.next = None
		self.prev = None


class LinkedDictItemIterator(object):
	def __init__(self, start, reverse=False):
		self.itr = start
		self.reverse = reverse

	def __iter__(self):
		return self

	def next(self):
		if self.itr is None:
			raise StopIteration

		key, val = self.itr.key, self.itr.val
		self.itr = self.itr.prev if self.reverse else self.itr.next
		return key, val

	def __next__(self):
		return self.next()


class LinkedDict(object):
	DICT_VAL_I = 0
	DICT_NODE_I = 1

	def __init__(self):
		self.dict = dict()
		self.head = None
		self.tail = None
		self.itr = None

	def __len__(self):
		return len(self.dict)

	def __iter__(self):
		self.itr = self.head
		return self

	def iteritems(self, reverse=False):
		itr = LinkedDictItemIterator(
			self.tail if reverse else self.head,
			reverse=reverse
		)
		return iter(itr)

	def next(self):
		if self.itr is None:
			raise StopIteration

		res = self.itr.key
		self.itr = self.itr.next
		return res

	def __next__(self):
		if self.itr is None:
			raise StopIteration

		res = self.itr.key
		self.itr = self.itr.next
		return res

	def __delitem__(self, key):
		if key not in self.dict:
			raise KeyError(key)

		node = self.dict[key][LinkedDict.DICT_NODE_I]
		if node is self.head:
			self.head = self.head.next
		if node is self.tail:
			self.tail = self.tail.prev

		prevNode = node.prev
		nextNode = node.next
		if prevNode:
			prevNode.next = nextNode
		if nextNode:
			nextNode.prev = prevNode


		del self.dict[key]

	def __getitem__(self, key):
		return self.dict[key][LinkedDict.DICT_VAL_I]

	def __setitem__(self, key, val):
		if key in self.dict:
			del self[key]

		if self.head is None:
			newNode = ListNode(key, val)
			self.head = newNode
			self.tail = self.head
		else:
			newNode = ListNode(key, val)
			newNode.prev = self.tail
			self.tail.next = newNode
			self.tail = newNode

		self.dict[key] = (val, newNode)

	def __str__(self):
		res = []
		for key, val in self.iteritems():
			res.append('%s:%s' % (str(key), str(val)))

		return '{%s}' % ", ".join(res)
