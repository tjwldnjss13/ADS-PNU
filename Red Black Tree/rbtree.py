
class RedBlackTree:
    class Node:
        def __init__(self, key, color='b'):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None
            self.color = color
            self.depth = 0

    def __init__(self):
        self.root = None
        self.N_key = 0

    def search(self, key):
        cur = self.root
        if cur is None:
            return None
        if cur.key == key:
            return cur
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur

    def insert(self, key):
        if self.root is None:
            node = self.Node(key)
            self.root = node
        else:
            if self.search(key) is None:
                cur = self.root
                parent = None
                while cur is not None:
                    parent = cur
                    if key < cur.key:
                        cur = cur.left
                    else:
                        cur = cur.right
                node = self.Node(key, color='r')
                if key < parent.key:
                    parent.left = node
                else:
                    parent.right = node
                node.parent = parent
                node.depth = parent.depth + 1

                # Reconstruct / Recolor conditions
                if node.parent.color == 'r':
                    self.balance(node)

    def balance(self, node):
        if node.depth >= 2:
            parent = node.parent
            gparent = parent.parent
            uncle = None
            if parent is gparent.left:
                uncle = gparent.right
            elif parent is gparent.right:
                uncle = gparent.left

            if uncle is None or (uncle is not None and uncle.color == 'b'):
                self.reconstruct(node)
            elif uncle is not None and uncle.color == 'r':
                self.recolor(node)

    def reconstruct(self, node):
        parent = node.parent
        gparent = parent.parent
        if parent is None:
            return
        if parent is gparent.left:
            if node is parent.right:
                # left rotate
                parent = self.rotate_left(parent)
            # right rotate
            gparent = parent.parent
            gparent = self.rotate_right(gparent)

            # Recolor
            gparent.color = 'b'
            gparent.right.color = 'r'

        elif parent is gparent.right:
            if node is parent.left:
                # right rotate
                parent = self.rotate_right(parent)
            # left rotate
            gparent = parent.parent
            gparent = self.rotate_left(gparent)

            # Recolor
            gparent.color = 'b'
            gparent.left.color = 'r'

    def recolor(self, node):
        parent = node.parent
        gparent = parent.parent
        uncle = None
        if parent is gparent.left:
            uncle = gparent.right
        elif parent is gparent.right:
            uncle = gparent.left

        parent.color = 'b'
        uncle.color = 'b'
        if gparent is self.root:
            gparent.color = 'b'
        else:
            gparent.color = 'r'

            if gparent.parent.color == 'r':
                self.balance(gparent)

    def rotate_left(self, node):
        if node.right is None:
            return

        if node is self.root:
            child_f = -1
        else:
            parent_temp = node.parent
            if node is parent_temp.left:
                child_f = 0
            else:
                child_f = 1

        new_subroot = node.right
        if child_f == -1:
            self.root = new_subroot
            self.root.parent = None
        else:
            new_subroot.parent = parent_temp
            if child_f == 0:
                parent_temp.left = new_subroot
            elif child_f == 1:
                parent_temp.right = new_subroot
        sub = new_subroot.left

        new_subroot.left = node
        node.parent = new_subroot
        new_subroot.left.right = sub

        self.reset_depth(new_subroot)

        return new_subroot

    def rotate_right(self, node):
        if node.left is None:
            return

        if node is self.root:
            child_f = -1
        else:
            parent_temp = node.parent
            if node is parent_temp.left:
                child_f = 0
            else:
                child_f = 1

        new_subroot = node.left
        if child_f == -1:
            self.root = new_subroot
            self.root.parent = None
        else:
            new_subroot.parent = parent_temp
            if child_f == 0:
                parent_temp.left = new_subroot
            elif child_f == 1:
                parent_temp.right = new_subroot
        sub = new_subroot.right

        new_subroot.right = node
        node.parent = new_subroot
        new_subroot.right.left = sub

        self.reset_depth(new_subroot)

        return new_subroot

    def reset_depth(self, node):
        if node is None:
            return
        self.reset_depth_util(node)

    def reset_depth_util(self, node):
        if node.parent is not None:
            node.depth = node.parent.depth + 1
        else:
            node.depth = 0
        if node.right is not None:
            self.reset_depth_util(node.right)
        if node.left is not None:
            self.reset_depth_util(node.left)

    def print_rbtree(self):
        self.print_rbtree_util(self.root)

    def print_rbtree_util(self, node):
        if node.right is not None:
            self.print_rbtree_util(node.right)
        print(node.depth * '       ', end='')
        print('{}:{}'.format(node.key, node.color))
        if node.left is not None:
            self.print_rbtree_util(node.left)


if __name__ == '__main__':
    # inputs = [300, 51, 624, 62, 153, 41, 623, 42, 6, 25, 7, 34, 745]
    inputs = [300, 51, 624, 62, 153, 41, 623, 42]

    rb = RedBlackTree()

    for input in inputs:
        rb.insert(int(input))
        rb.print_rbtree()
        print('-------------------------------------------')

    rb.insert(6)
