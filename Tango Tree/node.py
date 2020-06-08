
class Node:
    def __init__(self, key=None, color='b'):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.prefer = 1  # 0 : left child, 1 : right child
        self.color = color
        self.depth = 0
