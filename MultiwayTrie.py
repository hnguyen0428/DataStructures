class MultiwayTrieNode(object):
	def __init__(self, char=None):
		self.children = dict()
		self.isWord = False
		self.count = 0
		self.char = char

	def __iter__(self):
		return iter(self.children.values())

	def __contains__(self, char):
		return char in self.children

	def __getitem__(self, char):
		return self.children[char]

	def __setitem__(self, char, node):
		self.children[char] = node


class MultiwayTrie(object):
	def __init__(self):
		self.root = MultiwayTrieNode()
		self.wordsCount = 0

	def __contains__(self, word):
		return self.search(word)

	def __len__(self):
		return self.wordsCount

	def searchNode(self, word):
		if len(word) == 0: return None

		curr = self.root
		for char in word:
			if char in curr:
				curr = curr[char]
			else:
				return None

		return curr

	def search(self, word):
		node = self.searchNode(word)
		return False if node is None else node.isWord

	def searchWordCount(self, word):
		node = self.searchNode(word)
		if node is None:
			return -1

		return node.count if node.isWord else -1

	def insert(self, word):
		if len(word) == 0: return

		curr = self.root
		for char in word:
			if char in curr:
				curr = curr[char]
			else:
				newNode = MultiwayTrieNode(char)
				curr[char] = newNode
				curr = newNode

		curr.count += 1
		if not curr.isWord:
			self.wordsCount += 1
			curr.isWord = True

	def autocomplete(self, prefix, topN=10):
		node = self.searchNode(prefix)
		if node is None:
			return []

		stack = [(node, prefix[:-1])]
		results = []
		while len(stack) != 0:
			(node, prefix) = stack.pop()
			if node.isWord:
				results.append((node.count, prefix + node.char))

			for child in node:
				stack.append((child, prefix + node.char))

		# Sort by count
		results.sort(key=lambda val: val[0], reverse=True)
		return list(map(lambda val: val[1], results[:topN]))

