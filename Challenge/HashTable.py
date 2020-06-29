
class Node:
    def __init__(self, key):
        self.key = key
        self.next = None


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * self.size

    def hash_function(self, data):
        return data % self.size

    def insert(self, data, value):
        key = self.hash_function(data)
        if self.table[key] is None:
            self.table[key] = Node(value)
        else:
            node = Node(value)
            cur = self.table[key]
            while cur.next is not None:
                cur = cur.next
            cur.next = node

    def delete(self, data):
        key = self.hash_function(data)
        cur = self.table[key]

