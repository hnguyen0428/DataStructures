class Deque(object):    
    def __init__(self, initSize=10):
        self.queue = [None] * initSize
        self.front = 0
        self.rear = -1
        self.numEle = 0

    def addFront(self, val):
        if len(self.queue) == self.numEle:
            self.resize()

        if self.numEle == 0:
            self.addRear(val)
        else:
            self.front = len(self.queue) - 1 if self.front - 1 < 0 else self.front - 1
            self.queue[self.front] = val
            self.numEle += 1        

    def addRear(self, val):
        if len(self.queue) == self.numEle:
            self.resize()

        self.rear = (self.rear + 1) % len(self.queue)
        self.queue[self.rear] = val

        self.numEle += 1

    def removeFront(self):
        if self.numEle == 0:
            raise RuntimeError('Trying to remove from an empty queue.')

        res = self.queue[self.front]
        self.front = (self.front + 1) % len(self.queue)
        self.numEle -= 1

        return res

    def removeRear(self):
        if self.numEle == 0:
            raise RuntimeError('Trying to remove from an empty queue.')

        res = self.queue[self.rear]
        self.rear = len(self.queue) - 1 if self.rear - 1 < 0 else self.rear - 1
        self.numEle -= 1

        return res

    def peekFront(self):
        if self.numEle == 0:
            raise RuntimeError('Trying to peek an empty queue.')

        return self.queue[self.front]

    def peekRear(self):
        if self.numEle == 0:
            raise RuntimeError('Trying to peek an empty queue.')

        return self.queue[self.rear]

    def resize(self):
        newQueue = [None] * (len(self.queue) * 2)
        if self.front <= self.rear:
            newQueue[0:self.rear-self.front+1] = self.queue[self.front:self.rear+1]
        else:
            rightLen = len(self.queue)-self.front
            newQueue[0:rightLen] = self.queue[self.front:]
            newQueue[rightLen:rightLen+self.rear+1] = self.queue[:self.rear+1]

        self.queue = newQueue
        self.front = 0
        self.rear = self.numEle - 1

    def __str__(self):
        if self.numEle == 0:
            return '[]'

        res = []
        i = self.front
        while i != self.rear:
            res.append(str(self.queue[i]))
            i = (i + 1) % len(self.queue)

        res.append(self.queue[self.rear])
        return '[%s]' % ", ".join(res)

    def __len__(self):
        return self.numEle
