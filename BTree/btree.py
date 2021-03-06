import copy
import random
import time
import matplotlib.pyplot as plt


class BTree:
    class Node:
        def __init__(self, key):
            if type(key) == list:
                self.key = key
            else:
                self.key = [key]
            self.child = []

    def __init__(self, degree=3):
        self.root = None
        self.degree = degree
        self.N_key = 0
        self.N_dup = 0

    def create_node(self, key):
        node = self.Node(key)
        for i in range(self.degree):
            node.child.append(None)

        return node

    def search(self, key, node=None):
        if node is None:
            sub_root = self.root
        else:
            sub_root = node
        if sub_root is None:
            return None
        cur = sub_root
        while cur is not None:
            if key in cur.key:
                return cur
            if key < cur.key[0]:
                cur = cur.child[0]
                continue
            if key > cur.key[-1]:
                cur = cur.child[len(cur.key)]
                continue
            for i in range(1, len(cur.key)):
                if cur.key[i - 1] < key < cur.key[i]:
                    cur = cur.child[i]
                    break
        return None

    def insert(self, key):
        if self.search(key) is not None:
            self.N_dup += 1
            return
        if self.root is None:
            self.root = self.create_node(key)
            self.N_key += 1
            return
        next = self.root
        cur = None
        while next is not None:
            cur = next
            if key < cur.key[0]:
                next = cur.child[0]
                continue
            if key > cur.key[-1]:
                next = cur.child[len(cur.key)]
                continue
            for i in range(1, len(cur.key)):
                if cur.key[i - 1] < key < cur.key[i]:
                    next = cur.child[i]
        if len(cur.key) < self.degree - 1:
            if key < cur.key[0]:
                cur.key.insert(0, key)
                self.N_key += 1
                return
            for i in range(1, len(cur.key)):
                if cur.key[i - 1] < key < cur.key[i]:
                    cur.key.insert(i, key)
                    self.N_key += 1
                    return
            if key > cur.key[-1]:
                cur.key.append(key)
                self.N_key += 1
                return
        else:
            self.split(cur, key)
            self.N_key += 1

    def split(self, node, key, sub_child=[]):
        if len(sub_child) == 0:
            for i in range(self.degree + 1):
                sub_child.append(None)

        node_temp = copy.deepcopy(node)
        node_temp.key.append(key)
        node_temp.key.sort()

        if node is self.root:
            root_new = self.create_node(node_temp.key.pop(int((len(node_temp.key) - 1) / 2)))

            root_new.child[0] = self.create_node(key=copy.deepcopy(node_temp.key[:int(len(node_temp.key) / 2)]))
            root_new.child[1] = self.create_node(key=copy.deepcopy(node_temp.key[int(len(node_temp.key) / 2):]))
            for i in range(len(root_new.child[0].key) + 1):
                root_new.child[0].child[i] = sub_child.pop(0)
            for i in range(len(root_new.child[1].key) + 1):
                root_new.child[1].child[i] = sub_child.pop(0)
            self.root = root_new
            return

        parent = self.get_parent(node)
        key_mid = node_temp.key.pop(int((len(node_temp.key) - 1) / 2))

        if len(parent.key) < self.degree - 1:
            parent.key.append(key_mid)
            parent.key.sort()

            child_i = parent.key.index(key_mid)
            parent.child[child_i] = self.create_node(key=copy.deepcopy(node_temp.key[:int(len(node.key) / 2)]))
            parent.child.insert(child_i + 1, self.create_node(key=copy.deepcopy(node_temp.key[(int(len(node.key) / 2)):])))
            while len(parent.child) > self.degree:
                parent.child.pop(-1)
            for i in range(child_i, child_i + 2):
                for j in range(len(parent.child[i].key) + 1):
                    parent.child[i].child[j] = sub_child.pop(0)

        else:
            node1 = self.create_node(key=copy.deepcopy(node_temp.key[:int(len(node.key) / 2)]))
            node2 = self.create_node(key=copy.deepcopy(node_temp.key[int(len(node.key) / 2):]))

            for i in range(len(node1.key) + 1):
                node1.child[i] = sub_child.pop(0)
            for i in range(len(node2.key) + 1):
                node2.child[i] = sub_child.pop(0)

            child_i = parent.child.index(node)
            sub_child_new = []

            for i in range(self.degree):
                if i == child_i:
                    sub_child_new.append(node1)
                    sub_child_new.append(node2)
                else:
                    sub_child_new.append(parent.child[i])
            self.split(parent, key_mid, sub_child_new)

    def delete(self, key, node=None):
        # Cases
        # 1) Key is not in the tree
        # 2) Key is in a leaf note
        #    2-1) 1 Key in a leaf
        #    2-2) More than 1 key in a leaf
        # 3) Key is in an internal node
        #    3-1) 1 key in a node
        #    3-2) More than 1 key in a node

        target = self.search(key, node)
        parent = self.get_parent(target)

        # Case 1
        if target is None:
            return
        # Case 2
        if target.child[0] is None:
            # Case 2-1
            target.key.remove(key)
            if len(target.key) == 0:
                cur = target
                while len(cur.key) == 0:
                    if cur is self.root:
                        self.root = cur.child[0]
                        break
                    parent_next = self.get_parent(parent)
                    cur = self.merge(parent, cur)
                    parent = parent_next
                self.N_key -= 1
                return

            # Case 2-2
            else:
                self.N_key -= 1
                return
        # Case 3
        pre = self.get_predecessor(key)
        suc = self.get_successor(key)
        key_i = target.key.index(key)

        # Case 3-1
        if len(target.key) == 1:
            cur, parent = pre, self.get_parent(pre)
            target.key[key_i] = pre.key.pop(-1)

            while len(cur.key) == 0:
                if cur is self.root:
                    self.root = cur.child[0]
                    break
                parent_next = self.get_parent(parent)
                cur = self.merge(parent, cur)
                parent = parent_next
            self.N_key -= 1
            return

        # Case 3-2
        else:
            if len(pre.key) > 1:
                target.key[key_i] = pre.key.pop(-1)
                self.N_key -= 1
                return
            elif len(suc.key) > 1:
                target.key[key_i] = suc.key.pop(0)
                self.N_key -= 1
                return
            else:
                cur, parent = pre, self.get_parent(pre)
                target.key[key_i] = pre.key.pop(0)
                while len(cur.key) == 0:
                    if cur is self.root:
                        self.root = cur
                        break
                    parent_next = self.get_parent(parent)
                    cur = self.merge(parent, cur)
                    parent = parent_next
                self.N_key -= 1
                return

    def merge(self, parent, child_empty):
        child_empty_i = parent.child.index(child_empty)
        if child_empty_i == 0:
            child_merge_i = 1
            child_merge = parent.child[1]
        else:
            child_merge_i = child_empty_i - 1
            child_merge = parent.child[child_merge_i]

        sub_childs = []
        if child_empty_i < child_merge_i:
            sub_childs.append(child_empty.child[0])
            for i in range(len(child_merge.key) + 1):
                sub_childs.append(child_merge.child[i])

            child_empty.key.append(parent.key.pop(child_empty_i))
            if len(child_merge.key) > 1:
                parent.key.insert(child_empty_i, child_merge.key.pop(0))
            else:
                child_empty.key.append(child_merge.key.pop(0))

            if len(child_empty.key) > 0:
                for i in range(self.degree):
                    if i < len(child_empty.key) + 1:
                        child_empty.child[i] = sub_childs.pop(0)
                    else:
                        child_empty.child[i] = None
            if len(child_merge.key) > 0:
                for i in range(self.degree):
                    if i < len(child_merge.key) + 1:
                        child_merge.child[i] = sub_childs.pop(0)
                    else:
                        child_merge.child[i] = None
            if len(child_merge.key) == 0:
                parent.child.pop(child_merge_i)
                parent.child.append(None)

            return parent
        else:
            for i in range(len(child_merge.key) + 1):
                sub_childs.append(child_merge.child[i])
            sub_childs.append(child_empty.child[0])

            child_empty.key.append(parent.key.pop(child_merge_i))
            if len(child_merge.key) > 1:
                parent.key.insert(child_merge_i, child_merge.key.pop(-1))
            else:
                child_empty.key.insert(0, child_merge.key.pop(0))

            if len(child_merge.key) > 0:
                for i in range(self.degree):
                    if i < len(child_merge.key) + 1:
                        child_merge.child[i] = sub_childs.pop(0)
                    else:
                        child_merge.child[i] = None
            if len(child_empty.key) > 0:
                for i in range(self.degree):
                    if i < len(child_empty.key) + 1:
                        child_empty.child[i] = sub_childs.pop(0)
                    else:
                        child_empty.child[i] = None
            if len(child_merge.key) == 0:
                parent.child.pop(child_merge_i)
                parent.child.append(None)

            return parent


    def get_parent(self, node):
        if node is None:
            return None
        if node is self.root:
            return None
        key = node.key[0]
        cur = self.root
        parent = None
        while cur is not None:
            if cur is node:
                return parent
            parent = cur
            if key in cur.key:
                return parent
            if key < cur.key[0]:
                cur = cur.child[0]
                continue
            if key > cur.key[-1]:
                cur = cur.child[len(cur.key)]
                continue
            for i in range(1, len(cur.key)):
                if cur.key[i - 1] < key < cur.key[i]:
                    cur = cur.child[i]
                    break
        return None

    def get_predecessor(self, key):
        node = self.search(key)
        if node is None:
            return None
        if node.child[0] is None:
            return None
        key_i = node.key.index(key)
        cur = node.child[key_i]
        if cur is None:
            return None
        while cur.child[len(cur.key)] is not None:
            cur = cur.child[len(cur.key)]
        return cur

    def get_successor(self, key):
        node = self.search(key)
        if node is None:
            return None
        if node.child[0] is None:
            return None
        key_i = node.key.index(key)
        cur = node.child[key_i + 1]
        if cur is None:
            return None
        while cur.child[0] is not None:
            cur = cur.child[0]
        return cur

    @staticmethod
    def print_tree(tree):
        if tree.root is not None:
            BTree.print_tree_util(tree.root, 0)

    @staticmethod
    def print_tree_util(node, depth):
        if node.child[len(node.key)] is not None:
            BTree.print_tree_util(node.child[len(node.key)], depth + 1)
        for i in range(len(node.key) - 1, 0, -1):
            print('    ' * depth, end='')
            print(node.key[i])
            if node.child[i] is not None:
                BTree.print_tree_util(node.child[i], depth + 1)
        print('    ' * depth, end='')
        print(node.key[0])
        if node.child[0] is not None:
            BTree.print_tree_util(node.child[0], depth + 1)


if __name__ == '__main__':
    fn = 'input.txt'
    f = open(fn, 'r')
    datas = f.readlines()
    f.close()
    N_data_list = []
    for i in range(len(datas)):
        N_data_list.append(i + 1)
        datas[i] = int(datas[i])

    _23tree, _234tree = BTree(3), BTree(4)

    print('Inserting...')

    _23_insert_time = []
    start = time.time()
    for data in datas:
        _23tree.insert(data)
        mid = time.time()
        _23_insert_time.append(mid - start)

    _234_insert_time = []
    start = time.time()
    for data in datas:
        _234tree.insert(data)
        mid = time.time()
        _234_insert_time.append(mid - start)

    print('Inserting done')

    print('Searching...')

    _23_search_time = []
    start = time.time()
    for i in range(len(datas)):
        if i < int(len(datas) * .7):
            data_search = random.randint(1, len(datas))
        else:
            data_search = random.randint(len(datas) + 1, 2 * len(datas))
        _23tree.search(data_search)
        mid = time.time()
        _23_search_time.append(mid - start)

    _234_search_time = []
    start = time.time()
    for i in range(len(datas)):
        data_search = random.randint(1, len(datas))
        _234tree.search(data_search)
        mid = time.time()
        _234_search_time.append(mid - start)

    print('Searching done')

    print('Deleting...')

    _23_delete_time = []
    start = time.time()
    for i in range(int(len(datas) / 2)):
        _23tree.delete(datas[-1])
        mid = time.time()
        _23_delete_time.append(mid - start)

    N_delete_list = []
    _234_delete_time = []
    start = time.time()
    for i in range(int(len(datas) / 2)):
        _234tree.delete(datas[-1])
        mid = time.time()
        _234_delete_time.append(mid - start)
        N_delete_list.append(i + 1)

    print('Deleting done')

    print('[Insertion]')
    print('23 Tree  : {}'.format(_23_insert_time[-1]))
    print('234 Tree : {}'.format(_234_insert_time[-1]))

    print('\n[Search]')
    print('23 Tree  : {}'.format(_23_search_time[-1]))
    print('234 Tree : {}'.format(_234_search_time[-1]))

    print('\n[Deletion]')
    print('23 Tree  : {}'.format(_23_delete_time[-1]))
    print('234 Tree : {}'.format(_234_delete_time[-1]))

    plt.figure(0)
    plt.plot(N_data_list, _23_insert_time, 'r-', label='23 Tree')
    plt.plot(N_data_list, _234_insert_time, 'b:', label='234 Tree')
    plt.title('Insert time')
    plt.legend()

    plt.figure(1)
    plt.plot(N_data_list, _23_search_time, 'r-', label='23 Tree')
    plt.plot(N_data_list, _234_search_time, 'b:', label='234 Tree')
    plt.title('Search time')
    plt.legend()

    plt.figure(2)
    plt.plot(N_delete_list, _23_delete_time, 'r-', label='23 Tree')
    plt.plot(N_delete_list, _234_delete_time, 'b:', label='234 Tree')
    plt.title('Delete time')
    plt.legend()

    plt.show()

