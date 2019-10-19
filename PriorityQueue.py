from DHeap import DHeap


class PriorityQueue(object):
	def __init__(self, reverse=False):
		self.heap = DHeap(minHeap=not reverse)

	def __len__(self):
		return len(self.heap)

	def enqueue(self, val):
		self.heap.insert(val)

	def dequeue(self):
		return self.heap.pop()

	def front(self):
		return self.heap.peek()
