class DHeap(object):
	INIT_POWER = 4

	def __init__(self, d=2, minHeap=True):
		self.numEle = 0

		self.heap = [None] * d ** DHeap.INIT_POWER
		self.isMin = minHeap
		self.d = d 			# Number of children

	def getParentIndex(self, index):
		return int((index - 1) / self.d)

	def getChildrenIndices(self, index):
		base = self.d * index
		return [base + i for i in range(1, self.d + 1)]

	def cmp(self, lhs, rhs):
		return lhs < rhs if self.isMin else lhs > rhs


	def trickleDown(self, index):
		if index >= self.numEle:	# Invalid index
			return

		func = min if self.isMin else max

		chld = self.getChildrenIndices(index)
		if chld[-1] >= self.numEle:		# Already at leaf node
			return

		extreme = func(chld, key=lambda i: self.heap[i])

		# chld[-1] < self.numEle indicates that index is not yet at the leaf node
		while self.cmp(self.heap[extreme], self.heap[index]):
			self.heap[extreme], self.heap[index] = self.heap[index], self.heap[extreme]
			index = extreme
			chld = self.getChildrenIndices(index)
			if chld[-1] >= self.numEle:
				break

			extreme = func(chld, key=lambda i: self.heap[i])


	def bubbleUp(self, index):
		if index == 0:
			return

		prnt = self.getParentIndex(index)
		while index != 0 and self.cmp(self.heap[index], self.heap[prnt]):
			self.heap[prnt], self.heap[index] = self.heap[index], self.heap[prnt]
			index = prnt
			prnt = self.getParentIndex(index)


	def insert(self, val):
		if len(self.heap) == self.numEle: 	# Expand the heap by d
			newHeap = [None] * (len(self.heap) * self.d)
			newHeap[:self.numEle] = self.heap[:self.numEle]
			self.heap = newHeap

		# Insert at last element then bubble up
		self.heap[self.numEle] = val
		self.bubbleUp(self.numEle)
		self.numEle += 1


	def pop(self):
		if self.numEle == 0:
			raise RuntimeError('Trying to pop from an empty heap.')

		res = self.heap[0]
		self.heap[0] = self.heap[self.numEle-1]
		self.trickleDown(0)

		self.numEle -= 1
		self.heap[self.numEle] = None
		return res

	def peek(self):
		if self.numEle == 0:
			raise RuntimeError('Trying to peek an empty heap.')
		return self.heap[0]

	def __len__(self):
		return self.numEle
