from node import *


class BST:
    def __init__(self):
        self.root = None
        self.N_key = 0

    def search(self, key):
        cur = self.root
        if cur is None:
            return None
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur
        return None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
            return
        if self.search(data, self.root) is None:
            if self.root.data is None:
                self.root.data = data
                return self.root
            node = self.Node(data)
            parent = None
            current = self.root
            while current is not None:
                parent = current
                if data < current.data:
                    current = current.left
                else:
                    current = current.right

            if data < parent.data:
                parent.left = node
                node.depth = parent.depth + 1
            else:
                parent.right = node
                node.depth = parent.depth + 1
            return node
        return None

    def online_insert(self, inputs):
        for key in inputs:
            if self.search(key) is None:
                node = Node(key)
                if self.root is None:
                    self.root = node
                else:
                    cur = self.root
                    parent = None
                    while cur is not None:
                        parent = cur
                        if key < cur.key:
                            cur = cur.left
                        else:
                            cur = cur.right
                    node.depth = parent.depth + 1
                    if key < parent.key:
                        parent.left = node
                    else:
                        parent.right = node
                self.N_key += 1
