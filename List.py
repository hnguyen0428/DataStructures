class ListNode(object):
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

class ListIterator(object):
    def __init__(self, start):
        self.itr = start

    def __iter__(self):
        return self

    def next(self):
        if self.itr is None:
            raise StopIteration

        res = self.itr.val
        self.itr = self.itr.next
        return res


class List(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.numEle = 0

    def append(self, val):
        if self.head is None:
            self.head = ListNode(val)
            self.tail = self.head
        else:
            newNode = ListNode(val)
            newNode.prev = self.tail
            self.tail.next = newNode
            self.tail = newNode

        self.numEle += 1

    def prepend(self, val):
        if self.head is None:
            self.append(val)
        else:
            newNode = ListNode(val)
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode

        self.numEle += 1

    def extend(self, l):
        for val in l:
            self.append(val)

    def insert(self, val, i):
        if i < 0 or i >= self.numEle:
            raise RuntimeError('Invalid index.')

        curr = self.head
        while i > 0:
            curr = curr.next
            i -= 1

        newNode = ListNode(val)
        newNode.next = curr
        newNode.prev = curr.prev
        curr.prev = newNode
        self.numEle += 1

    def remove(self, val):
        if self.numEle == 0:
            raise RuntimeError('List is empty')

        curr = self.head
        while curr.val != val:
            curr = curr.next

        if curr is not None:
            if curr is self.head:
                self.head = self.head.next
            if curr is self.tail:
                self.tail = self.tail.prev

            nextNode = curr.next
            prevNode = curr.prev
            if nextNode:
                nextNode.prev = prevNode
            if prevNode:
                prevNode.next = nextNode

            self.numEle -= 1
        else:
            raise RuntimeError('List does not contain element being removed')

    def popFront(self):
        if self.numEle == 0:
            raise RuntimeError('List is empty')

        res = self.head.val
        nextNode = self.head.next
        if nextNode:
            nextNode.prev = None

        self.head = nextNode
        self.numEle -= 1
        return res

    def popRear(self):
        if self.numEle == 0:
            raise RuntimeError('List is empty')

        res = self.tail.val
        prevNode = self.tail.prev
        if prevNode:
            prevNode.next = None

        self.tail = prevNode
        self.numEle -= 1
        return res

    def peekFront(self):
        if self.numEle == 0:
            raise RuntimeError('List is empty')

        return self.head.val

    def peekRear(self):
        if self.numEle == 0:
            raise RuntimeError('List is empty')

        return self.tail.val

    def __getitem__(self, i):
        if i < 0 or i >= self.numEle:
            raise RuntimeError('Invalid index.')

        curr = self.head
        while i > 0:
            curr = curr.next
            i -= 1

        return curr.val

    def __str__(self):
        if self.numEle == 0:
            return '[]'

        res = []
        curr = self.head
        while curr is not None:
            res.append(str(curr.val))
            curr = curr.next

        return '[%s]' % ", ".join(res)

    def __contains__(self, item):
        curr = self.head
        while curr is not None:
            if item == curr.val:
                return True
            curr = curr.next

        return False

    def __iter__(self):
        return ListIterator(self.head)

    def __next__(self):
        if self.itr is None:
            raise StopIteration

        res = self.itr.val
        self.itr = self.itr.next
        return res

    def __len__(self):
        return self.numEle
        
