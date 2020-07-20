class Node:

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class Stack:

    def __init__(self, limit):
        self.head = None
        self.tail = None
        self.limit = limit
        self.size = 0

    def push(self, item):

        temp = Node(item)

        if self.size == 0:
            self.head = self.tail = temp
        else:
            self.tail.next = temp
            temp.prev = self.tail
            self.tail = temp

        if self.size < self.limit:
            self.size += 1
        else:
            self.head = self.head.next
            self.head.prev = None

    def pop(self):

        if self.isEmpty():
            return None

        data =  self.tail.data
        self.tail = self.tail.prev

        if self.size <= 1:
            self.head = self.tail = None

        if self.size > 0:
            self.size -= 1

        return data

    def peek(self):
        return self.tail.data

    def size(self):
        return self.size

    def isEmpty(self):
        return self.size <= 0

'''
st = Stack(5)
for i in range(10):
    st.push(i)

start = st.head
while(start is not None):
    print(start.data)
    start = start.next

for i in range(10):
    print(st.pop())

for i in range(10):
    st.push(10)
    print(st.peek())
'''
