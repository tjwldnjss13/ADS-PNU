import random
import math
from node import *
from rbtree import *


class TangoTree:
    # class Node:
    #     def __init__(self, key):
    #         self.key = key
    #         self.left = None
    #         self.right = None
    #         self.prefer = 1   # 0 : left child, 1 : right child
    #         self.depth = 0

    search_cnt = 0

    def __init__(self, inputs):
        self.root = None
        self.N_key = 0
        self.online_insert(inputs)
        self.aux = None

    # def search(self, key):
    #     global search_cnt
    #
    #     cur = self.root
    #     while cur is not None:
    #         if key < cur.key:
    #             cur = cur.left
    #         elif key > cur.key:
    #             cur = cur.right
    #         else:
    #             return cur
    #     return None

    def tango_search(self, key):
        cur = self.aux.root
        target = None
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                target = cur
        target = None
        self.tango_update()

        return target

    def tango_update(self):
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





    # def preferred_path(self, node):
    #     cur = node
    #     path = []
    #     while cur is not None:
    #         path.append(cur.key)
    #         if cur.prefer == 0:
    #             cur = cur.left
    #         elif cur.prefer == 1:
    #             cur = cur.right
    #
    #     return path

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

    def print_tango(self):
        self.print_util(self.root)

    def print_util(self, node):
        if node.right is not None:
            self.print_util(node.right)
        print('      ' * node.depth, end='')
        print(node.key)
        if node.left is not None:
            self.print_util(node.left)


if __name__ == '__main__':
    fn = 'input0.txt'
    f = open(fn, 'r')
    inputs = f.readlines()
    f.close()

    print('Inserting...')
    for i in range(len(inputs)):
        inputs[i] = int(inputs[i])

    tango = TangoTree(inputs)
    tango.print_tango()

    # print('Searching...')
    # for i in range(len(inputs)):
    #     num = random.randint(1, len(inputs))
    #     tango.search(num)

    path_root = tango.preferred_path(tango.root)
    print(path_root)

