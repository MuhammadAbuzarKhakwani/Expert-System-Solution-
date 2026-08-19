class CircularQueue:
    def __init__(self, capacity):
        self.items = [None] * capacity #shuru main zara none dal dain idhr
        self.capacity = capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def enqueue(self, data):
        if self.is_full():
            print("Queue is full")
            return

        # Move rear forward circularly asal logic
        self.rear = (self.rear + 1) % self.capacity

        self.items[self.rear] = data
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return

        data = self.items[self.front]
        self.items[self.front] = None

        # Move front forward circularly asal kam ki  baat
        self.front = (self.front + 1) % self.capacity

        self.size -= 1
        return data

    def peek(self):
        if self.is_empty():
            print("Queue is empty")
            return

        return self.items[self.front]

    def display(self):
        print(self.items)

c1 = CircularQueue(3)

c1.enqueue(10)
c1.enqueue(20)

c1.display()

c1.dequeue()

c1.display()

c1.enqueue(30)

