
class Node:
    def __init__(self, ptn):
        self.ptn = ptn
        self.left = None
        self.right = None
        self.range = (None, None)
        self.bst_y = BinarySearchTreePtn(1)


class BinarySearchTreePtn:
    def __init__(self, xy_idx):
        self.root = None
        self.xy_idx = xy_idx

    def insert(self, ptn):
        if self.root is None:
            self.root = Node(ptn)
            return
        node = Node(ptn)
        cur = self.root
        parent = None
        while cur is not None:
            parent = cur
            if ptn[self.xy_idx] < cur.ptn[self.xy_idx]:
                cur = cur.left
            elif ptn[self.xy_idx] > cur.ptn[self.xy_idx]:
                cur = cur.right
        if ptn[self.xy_idx] < parent.ptn[self.xy_idx]:
            parent.left = node
        elif ptn[self.xy_idx] > parent.ptn[self.xy_idx]:
            parent.right = node

    def delete(self, ptn):
        if self.root is None:
            return
        target = self.root
        parent = None
        while target.ptn[0] != ptn[0] and target.ptn[1] != ptn[1]:
            parent = target
            if ptn[self.xy_idx] < target.ptn[self.xy_idx]:
                target = target.left
            elif ptn[self.xy_idx] > target.ptn[self.xy_idx]:
                target = target.right

        if target.left is None and target.right is None:
            if target is parent.left:
                parent.left = None
            else:
                parent.right = None
        elif target.left is None and target.right is not None:
            if target is parent.left:
                parent.left = target.right
            else:
                parent.right = target.right
        elif target.left is not None and target.right is None:
            if target is parent.left:
                parent.left = target.left
            else:
                parent.right = target.left
        else:
            pre = target.left
            parent_of_pre = target
            while pre.right is not None:
                parent_of_pre = pre
                pre = pre.right
            if target is parent.left:
                parent.left = pre
            else:
                parent.right = pre
            parent_of_pre.right = None

    def print_tree(self):
        BinarySearchTreePtn.print_tree_util(self.root, 0)

    @staticmethod
    def print_tree_util(node, depth):
        if node.right is not None:
            BinarySearchTreePtn.print_tree_util(node.right, depth + 1)
        print('          ' * depth, end='')
        print('({}, {})'.format(node.ptn[0], node.ptn[1]))
        if node.left is not None:
            BinarySearchTreePtn.print_tree_util(node.left, depth + 1)



