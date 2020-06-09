from rbtree import *
import time


class TangoTree:

    def __init__(self, inputs):
        self.root = None
        self.N_key = 0
        self.online_insert(inputs)
        self.aux = None

    def search(self, key):
        global search_cnt

        cur = self.root
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur
        return None

    def tango_search(self, key):
        # Find key in auxiliary tango tree
        if self.aux is not None:
            start = time.time()
            cur = self.aux.root
            while cur is not None:
                if key < cur.key:
                    cur = cur.left
                elif key > cur.key:
                    cur = cur.right
                else:
                    break
            end = time.time()
            if cur is None:
                return end - start
        else:
            start = time.time()
            cur = self.root
            parent = None
            while cur is not None:
                if key < cur.key:
                    parent = cur
                    cur = cur.left
                    parent.prefer = 0
                elif key > cur.key:
                    parent = cur
                    cur = cur.right
                    parent.prefer = 1
                else:
                    break
            end = time.time()
            if cur is None:
                return end - start

        # Update preferred paths
        cur = self.root
        parent = None
        while cur is not None:
            if key < cur.key:
                parent = cur
                cur = cur.left
                parent.prefer = 0
            elif key > cur.key:
                parent = cur
                cur = cur.right
                parent.prefer = 1
            else:
                break

        self.tango_update()

        return end - start

    def tango_update(self):
        # Make a list of preferred paths
        aux_paths = [[self.root.key]]
        ap_i = 0
        while ap_i < len(aux_paths):
            cur = self.search(aux_paths[ap_i][0])
            while cur is not None:
                if cur.prefer == 0:
                    if cur.left is not None:
                        aux_paths[ap_i].append(cur.left.key)
                    if cur.right is not None:
                        aux_paths.append([cur.right.key])
                    cur = cur.left
                elif cur.prefer == 1:
                    if cur.right is not None:
                        aux_paths[ap_i].append(cur.right.key)
                    if cur.left is not None:
                        aux_paths.append([cur.left.key])
                    cur = cur.right
            ap_i += 1

        # Make auxiliary trees of preferred paths
        n_aux = len(aux_paths)
        aux_trees =[]
        for at_i in range(n_aux):
            rbtree = RedBlackTree()
            for key in aux_paths[at_i]:
                rbtree.insert(key)
            aux_trees.append(rbtree)

        # Make a spare Tango tree
        self.aux = aux_trees[0]
        for i in range(1, n_aux):
            key = aux_trees[i].root.key
            cur = self.aux.root
            parent = None
            while cur is not None:
                parent = cur
                if key < cur.key:
                    cur = cur.left
                elif key > cur.key:
                    cur = cur.right
            if key < parent.key:
                parent.left = aux_trees[i].root
            else:
                parent.right = aux_trees[i].root

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

    def find_parent(self, key):
        cur = self.root
        parent = None
        while cur.key != key and cur is not None:
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
        if cur is parent.left:
            return parent, 0
        elif cur is parent.right:
            return parent, 1
        else:
            return None, -1

    @staticmethod
    def print_tree(tree):
        if tree is None:
            return
        TangoTree.print_util(tree.root, 0)

    @staticmethod
    def print_util(node, depth):
        if node.right is not None:
            TangoTree.print_util(node.right, depth + 1)
        print('      ' * depth, end='')
        print(node.key)
        if node.left is not None:
            TangoTree.print_util(node.left, depth + 1)


