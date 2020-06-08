from math import *


class BinomialHeap:
    class Node:
        def __init__(self, order=0, key=None):
            self.key = key
            self.parent = None
            self.sibling = None
            self.child = None
            self.order = order

    def __init__(self):
        self.trees = []
        self.total_node = 0

    def insert(self, key):
        if len(self.trees) == 0:
            new_root = self.Node(key=key)
            self.trees.append(new_root)
            self.total_node += 1
        else:
            new_heap = BinomialHeap()
            new_heap.trees.append(new_heap.Node(key=key))
            new_heap.total_node += 1
            self.merge(self, new_heap)

    def find_min(self):
        min_idx = 0
        for i in range(len(self.trees)):
            if self.trees[i].key <= self.trees[min_idx].key:
                min_idx = i
        return min_idx, self.trees[min_idx]

    def delete_min(self):
        tar_idx, _ = self.find_min()
        heap_subs = BinomialHeap()

        heap_subs.trees = BinomialHeap.subtree(self.trees[tar_idx])

        self.trees.pop(tar_idx)
        self.total_node -= 1
        BinomialHeap.merge(self, heap_subs)

    def delete(self):
        pass

    def decrease_key(self, node, new_key):
        if node.key <= new_key:
            return
        node.key = new_key
        while node.parent is not None:
            if node.parent.key > node.key:
                node.parent.key, node.key = node.key, node.parent.key
            node = node.parent



    @staticmethod
    def subtree(node):
        subs = []
        cur = node.child
        iter = node.order
        for i in range(iter):
            subs.insert(0, cur)
            if cur.sibling is not None:
                cur = cur.sibling
        for root in subs:
            root.sibling = None
        return subs

    @staticmethod
    def merge(bh1, bh2):
        if len(bh1.trees) is 0:
            bh1.trees = bh2.trees
            bh1.total_node = bh2.total_node
        elif len(bh2.trees) is 0:
            return bh1
        else:
            for j in range(len(bh2.trees)):
                for i in range(len(bh1.trees)):
                    if bh1.trees[i].order >= bh2.trees[j].order:
                        bh1.trees.insert(i, bh2.trees[j])
                        # bh1.total_node += bh2.trees[j].num_node
                        break
                    if i is len(bh1.trees) - 1:
                        bh1.trees.append(bh2.trees[j])

            bh1.total_node += bh2.total_node
            BinomialHeap.merge_util(bh1)
        return bh1

    @staticmethod
    def merge_util(heap):
        i = 0
        while i < len(heap.trees) - 1:
            if heap.trees[i].order < heap.trees[i + 1].order:
                i += 1
                continue
            elif heap.trees[i].order > heap.trees[i + 1].order:
                heap.trees[i], heap.trees[i + 1] = heap.trees[i + 1], heap.trees[i]
                i += 1
                continue
            else:
                if i + 2 <= len(heap.trees) - 1 and heap.trees[i + 1].order is heap.trees[i + 2].order:
                    i += 1
                    continue
                else:
                    if heap.trees[i].key <= heap.trees[i + 1].key:
                        if heap.trees[i].child is not None:
                            heap.trees[i + 1].sibling = heap.trees[i].child
                        heap.trees[i].child = heap.trees[i + 1]
                        heap.trees[i + 1].parent = heap.trees[i]
                        heap.trees[i].order += 1
                        heap.trees.pop(i + 1)
                    else:
                        heap.trees[i].sibling = heap.trees[i + 1].child
                        heap.trees[i + 1].child = heap.trees[i]
                        heap.trees[i].parent = heap.trees[i + 1]
                        heap.trees[i + 1].order += 1
                        heap.trees.pop(i)


    @staticmethod
    def self_merge(heap):
        i = 0
        while i < len(heap.trees) - 1:
            if heap.trees[i].order < heap.trees[i + 1].order:
                i += 1
                continue
            if heap.trees[i].order == heap.trees[i + 1].order:
                if heap.trees[i].key < heap.trees[i + 1].key:
                    heap.trees[i + 1].sibling = heap.trees[i].child
                    heap.trees[i].child, heap.trees[i + 1].parent = heap.trees[i + 1], heap.trees[i]
                    heap.trees[i].order += 1
                    heap.trees.pop(i + 1)
                else:
                    heap.trees[i].sibling = heap.trees[i + 1].child
                    heap.trees[i + 1].child, heap.trees[i].parent = heap.trees[i], heap.trees[i + 1]
                    heap.trees[i + 1].order += 1
                    heap.trees.pop(i)
            else:
                heap.trees[i], heap.trees[i + 1] = heap.trees[i + 1], heap.trees[i]
                i += 1

    @staticmethod
    def match_sibling(tree1, tree2):
        k = 0
        while k < tree1.order:
            node1, node2 = tree1, tree2.child
            for j in range(k):
                node1, node2 = node1.child, node2.child
            while node1.sibling is not None:
                node1 = node1.sibling
            node1.sibling = node2
            k += 1

    def print_heap(self):
        for tree in self.trees:
            print('<' + str(tree.order) + '>')
            self.print_heap_tree(tree)

    @staticmethod
    def print_heap_tree(tree):
        cur1 = tree
        k = tree.order
        if k == 0:
            print(cur1.key)
        else:
            while cur1 is not None:
                cur2 = cur1
                print('\t' * int(max(pow(2, k - 1) - 1, 0)), end='')
                while True:
                    print(str(cur2.key), end='\t')
                    if cur2.sibling is not None:
                        cur2 = cur2.sibling
                    else:
                        if cur2.parent is not None:
                            if cur2.parent.sibling is not None:
                                if cur2.parent.sibling.child is not None:
                                    cur2 = cur2.parent.sibling.child
                                else:
                                    break
                            else:
                                break
                        else:
                            break

                print()
                cur1 = cur1.child
                k -= 1