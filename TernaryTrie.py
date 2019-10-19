class TernaryTrieNode(object):
    def __init__(self, char):
        self.isWord = False
        self.count = 0

        self.left = None
        self.mid = None
        self.right = None

        self.char = char


class TernaryTrie(object):
    def __init__(self):
        self.root = None
        self.wordsCount = 0

    def __len__(self):
        return self.wordsCount

    ###
    ### RECURSIVE SEARCH
    ###
    # def searchNodeHelper(self, node, word, idx):
    #   if node is None:
    #       return None

    #   if word[idx] == node.char:
    #       if idx == len(word) - 1:
    #           return node

    #       return self.searchNodeHelper(node.mid, word, idx+1)
    #   elif word[idx] < node.char:
    #       return self.searchNodeHelper(node.left, word, idx)
    #   else:
    #       return self.searchNodeHelper(node.right, word, idx)

    # def searchNode(self, word):
    #   assert isinstance(word, str) and len(word) > 0
    #   return self.searchNodeHelper(self.root, word, 0)

    ###
    ### RECURSIVE INSERT
    ###
    # def insertHelper(self, node, word, idx):
    #   if node is None:
    #       node = TernaryTrieNode(word[idx])

    #   if word[idx] == node.char:
    #       if idx == len(word) - 1:
    #           if not node.isWord:
    #               self.wordsCount += 1
    #               node.isWord = True

    #           node.count += 1
    #       else:
    #           node.mid = self.insertHelper(node.mid, word, idx + 1)
    #   elif word[idx] < node.char:
    #       node.left = self.insertHelper(node.left, word, idx)
    #   else:
    #       node.right = self.insertHelper(node.right, word, idx)

    #   return node

    # def insert(self, word):
    #   assert isinstance(word, str) and len(word) > 0

    #   node = self.insertHelper(self.root, word, 0)
    #   if self.root is None:
    #       self.root = node


    ###
    ### ITERATIVE SEARCH
    ###
    def searchNode(self, word):
        if len(word) == 0: return None

        curr = self.root
        if curr is None:
            return None

        i = 0
        while i < len(word) and curr is not None:
            char = word[i]
            if char == curr.char:
                if i == len(word) - 1:
                    return curr
                curr = curr.mid
                i += 1
            elif char < curr.char:
                curr = curr.left
            else:
                curr = curr.right

        return curr

    def search(self, word):
        node = self.searchNode(word)
        return False if node is None else node.isWord

    def searchWordCount(self, word):
        node = self.searchNode(word)
        if node is None:
            return -1

        return node.count if node.isWord else -1

    ###
    ### ITERATIVE INSERT
    ###
    def insert(self, word):
        if len(word) == 0: return

        if self.root is None:
            self.root = TernaryTrieNode(word[0])
            
        curr = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char == curr.char:
                if i == len(word) - 1:
                    break

                i += 1
                if curr.mid is None:
                    curr.mid = TernaryTrieNode(word[i])

                curr = curr.mid
            elif char < curr.char:
                if curr.left is None:
                    curr.left = TernaryTrieNode(char)

                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = TernaryTrieNode(char)

                curr = curr.right

        if not curr.isWord:
            curr.isWord = True
            self.wordsCount += 1

        curr.count += 1

    def autocomplete(self, prefix, topN=10):
        node = self.searchNode(prefix)
        if node is None:
            return []

        results = []
        if node.isWord:
            results.append((node.count, prefix))

        if node.mid:
            stack = [(node.mid, prefix)]
            while len(stack) != 0:
                (node, prefix) = stack.pop()
                if node.isWord:
                    results.append((node.count, prefix + node.char))

                if node.mid:
                    stack.append((node.mid, prefix + node.char))
                if node.left:
                    stack.append((node.left, prefix))
                if node.right:
                    stack.append((node.right, prefix))

        # Sort by count
        results.sort(key=lambda val: val[0], reverse=True)
        return list(map(lambda val: val[1], results[:topN]))

