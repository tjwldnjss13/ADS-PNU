import copy
import random
import time
import matplotlib.pyplot as plt


class Node:
    def __init__(self, pnt):
        if type(pnt) == list:
            self.pnt = pnt
        else:
            self.pnt = [pnt]
        self.child = []
        self.range_tree_y = None


class BTreePnt:
    def __init__(self, degree=3, xy_idx=0):
        self.root = None
        self.degree = degree
        self.xy_idx = xy_idx
        self.N_pnt = 0
        self.N_dup = 0

    def create_node(self, pnt):
        node = self.Node(pnt)
        for i in range(self.degree):
            node.child.append(None)

        return node

    def search(self, pnt, node=None):
        if node is None:
            sub_root = self.root
        else:
            sub_root = node
        if sub_root is None:
            return None
        cur = sub_root
        while cur is not None:
            if pnt in cur.pnt:
                return cur
            if pnt[self.xy_idx] < cur.pnt[0][self.xy_idx]:
                cur = cur.child[0]
                continue
            if pnt[self.xy_idx] > cur.pnt[-1][self.xy_idx]:
                cur = cur.child[len(cur.pnt)]
                continue
            for i in range(1, len(cur.pnt)):
                if cur.pnt[i - 1][self.xy_idx] < pnt[self.xy_idx] < cur.pnt[i][self.xy_idx]:
                    cur = cur.child[i]
                    break
        return None

    def insert(self, pnt):
        if self.search(pnt) is not None:
            self.N_dup += 1
            return
        if self.root is None:
            self.root = self.create_node(pnt)
            if self.xy_idx == 0:
                self.root.range_tree_y = BTreePnt(self.degree, 1)
            self.N_pnt += 1
            return
        next = self.root
        cur = None
        while next is not None:
            cur = next
            if pnt[self.xy_idx] < cur.pnt[0][self.xy_idx]:
                next = cur.child[0]
                continue
            if pnt[self.xy_idx] > cur.pnt[-1][self.xy_idx]:
                next = cur.child[len(cur.pnt)]
                continue
            for i in range(1, len(cur.pnt)):
                if cur.pnt[i - 1][self.xy_idx] < pnt[self.xy_idx] < cur.pnt[i][self.xy_idx]:
                    next = cur.child[i]
        if len(cur.pnt) < self.degree - 1:
            if pnt[self.xy_idx] < cur.pnt[0][self.xy_idx]:
                cur.pnt.insert(0, pnt)
                if self.xy_idx == 0:
                    pass
                self.N_pnt += 1
                return
            for i in range(1, len(cur.pnt)):
                if cur.pnt[i - 1][self.xy_idx] < pnt[self.xy_idx] < cur.pnt[i][self.xy_idx]:
                    cur.pnt.insert(i, pnt)
                    self.N_pnt += 1
                    return
            if pnt[self.xy_idx] > cur.pnt[-1][self.xy_idx]:
                cur.pnt.append(pnt)
                self.N_pnt += 1
                return
        else:
            self.split(cur, pnt)
            self.N_pnt += 1

    def insert_to_sub_range_tree(self, png):
        pass

    def split(self, node, pnt, sub_child=[]):
        if len(sub_child) == 0:
            for i in range(self.degree + 1):
                sub_child.append(None)

        node_temp = copy.deepcopy(node)
        node_temp.pnt.append(pnt)
        node_temp.pnt.sort()

        if node is self.root:
            root_new = self.create_node(node_temp.pnt.pop(int((len(node_temp.pnt) - 1) / 2)))

            root_new.child[0] = self.create_node(key=copy.deepcopy(node_temp.pnt[:int(len(node_temp.pnt) / 2)]))
            root_new.child[1] = self.create_node(key=copy.deepcopy(node_temp.pnt[int(len(node_temp.pnt) / 2):]))
            for i in range(len(root_new.child[0].pnt) + 1):
                root_new.child[0].child[i] = sub_child.pop(0)
            for i in range(len(root_new.child[1].pnt) + 1):
                root_new.child[1].child[i] = sub_child.pop(0)
            self.root = root_new
            return

        parent = self.get_parent(node)
        pnt_mid = node_temp.pnt.pop(int((len(node_temp.pnt) - 1) / 2))

        if len(parent.pnt) < self.degree - 1:
            parent.pnt.append(pnt_mid)
            parent.pnt.sort()

            child_i = parent.pnt.index(pnt_mid)
            parent.child[child_i] = self.create_node(key=copy.deepcopy(node_temp.pnt[:int(len(node.pnt) / 2)]))
            parent.child.insert(child_i + 1, self.create_node(key=copy.deepcopy(node_temp.pnt[(int(len(node.pnt) / 2)):])))
            while len(parent.child) > self.degree:
                parent.child.pop(-1)
            for i in range(child_i, child_i + 2):
                for j in range(len(parent.child[i].pnt) + 1):
                    parent.child[i].child[j] = sub_child.pop(0)

        else:
            node1 = self.create_node(key=copy.deepcopy(node_temp.pnt[:int(len(node.pnt) / 2)]))
            node2 = self.create_node(key=copy.deepcopy(node_temp.pnt[int(len(node.pnt) / 2):]))

            for i in range(len(node1.pnt) + 1):
                node1.child[i] = sub_child.pop(0)
            for i in range(len(node2.pnt) + 1):
                node2.child[i] = sub_child.pop(0)

            child_i = parent.child.index(node)
            sub_child_new = []

            for i in range(self.degree):
                if i == child_i:
                    sub_child_new.append(node1)
                    sub_child_new.append(node2)
                else:
                    sub_child_new.append(parent.child[i])
            self.split(parent, pnt_mid, sub_child_new)

    def delete(self, pnt, node=None):
        # Cases
        # 1) Key is not in the tree
        # 2) Key is in a leaf note
        #    2-1) 1 Key in a leaf
        #    2-2) More than 1 key in a leaf
        # 3) Key is in an internal node
        #    3-1) 1 key in a node
        #    3-2) More than 1 key in a node

        target = self.search(pnt, node)
        parent = self.get_parent(target)

        # Case 1
        if target is None:
            return
        # Case 2
        if target.child[0] is None:
            # Case 2-1
            target.pnt.remove(pnt)
            if len(target.pnt) == 0:
                cur = target
                while len(cur.pnt) == 0:
                    if cur is self.root:
                        self.root = cur.child[0]
                        break
                    parent_next = self.get_parent(parent)
                    cur = self.merge(parent, cur)
                    parent = parent_next
                self.N_pnt -= 1
                return

            # Case 2-2
            else:
                self.N_pnt -= 1
                return
        # Case 3
        pre = self.get_predecessor(pnt)
        suc = self.get_successor(pnt)
        pnt_i = target.pnt.index(pnt)

        # Case 3-1
        if len(target.pnt) == 1:
            cur, parent = pre, self.get_parent(pre)
            target.pnt[pnt_i] = pre.pnt.pop(-1)

            while len(cur.pnt) == 0:
                if cur is self.root:
                    self.root = cur.child[0]
                    break
                parent_next = self.get_parent(parent)
                cur = self.merge(parent, cur)
                parent = parent_next
            self.N_pnt -= 1
            return

        # Case 3-2
        else:
            if len(pre.pnt) > 1:
                target.pnt[pnt_i] = pre.pnt.pop(-1)
                self.N_pnt -= 1
                return
            elif len(suc.pnt) > 1:
                target.pnt[pnt_i] = suc.pnt.pop(0)
                self.N_pnt -= 1
                return
            else:
                cur, parent = pre, self.get_parent(pre)
                target.pnt[pnt_i] = pre.pnt.pop(0)
                while len(cur.pnt) == 0:
                    if cur is self.root:
                        self.root = cur
                        break
                    parent_next = self.get_parent(parent)
                    cur = self.merge(parent, cur)
                    parent = parent_next
                self.N_pnt -= 1
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
            for i in range(len(child_merge.pnt) + 1):
                sub_childs.append(child_merge.child[i])

            child_empty.pnt.append(parent.pnt.pop(child_empty_i))
            if len(child_merge.pnt) > 1:
                parent.pnt.insert(child_empty_i, child_merge.pnt.pop(0))
            else:
                child_empty.pnt.append(child_merge.pnt.pop(0))

            if len(child_empty.pnt) > 0:
                for i in range(self.degree):
                    if i < len(child_empty.pnt) + 1:
                        child_empty.child[i] = sub_childs.pop(0)
                    else:
                        child_empty.child[i] = None
            if len(child_merge.pnt) > 0:
                for i in range(self.degree):
                    if i < len(child_merge.pnt) + 1:
                        child_merge.child[i] = sub_childs.pop(0)
                    else:
                        child_merge.child[i] = None
            if len(child_merge.pnt) == 0:
                parent.child.pop(child_merge_i)
                parent.child.append(None)

            return parent
        else:
            for i in range(len(child_merge.pnt) + 1):
                sub_childs.append(child_merge.child[i])
            sub_childs.append(child_empty.child[0])

            child_empty.pnt.append(parent.pnt.pop(child_merge_i))
            if len(child_merge.pnt) > 1:
                parent.key.insert(child_merge_i, child_merge.pnt.pop(-1))
            else:
                child_empty.pnt.insert(0, child_merge.pnt.pop(0))

            if len(child_merge.pnt) > 0:
                for i in range(self.degree):
                    if i < len(child_merge.pnt) + 1:
                        child_merge.child[i] = sub_childs.pop(0)
                    else:
                        child_merge.child[i] = None
            if len(child_empty.pnt) > 0:
                for i in range(self.degree):
                    if i < len(child_empty.pnt) + 1:
                        child_empty.child[i] = sub_childs.pop(0)
                    else:
                        child_empty.child[i] = None
            if len(child_merge.pnt) == 0:
                parent.child.pop(child_merge_i)
                parent.child.append(None)

            return parent

    def get_parent(self, node):
        if node is None:
            return None
        if node is self.root:
            return None
        pnt = node.pnt[0]
        cur = self.root
        parent = None
        while cur is not None:
            if cur is node:
                return parent
            parent = cur
            if pnt in cur.pnt:
                return parent
            if pnt[self.xy_idx] < cur.pnt[0]:
                cur = cur.child[0]
                continue
            if pnt[self.xy_idx] > cur.pnt[-1][self.xy_idx]:
                cur = cur.child[len(cur.pnt)]
                continue
            for i in range(1, len(cur.pnt)):
                if cur.pnt[i - 1][self.xy_idx] < pnt[self.xy_idx] < cur.pnt[i][self.xy_idx]:
                    cur = cur.child[i]
                    break
        return None

    def get_predecessor(self, pnt):
        node = self.search(pnt)
        if node is None:
            return None
        if node.child[0] is None:
            return None
        pnt_i = node.pnt.index(pnt)
        cur = node.child[pnt_i]
        if cur is None:
            return None
        while cur.child[len(cur.pnt)] is not None:
            cur = cur.child[len(cur.pnt)]
        return cur

    def get_successor(self, pnt):
        node = self.search(pnt)
        if node is None:
            return None
        if node.child[0] is None:
            return None
        pnt_i = node.pnt.index(pnt)
        cur = node.child[pnt_i + 1]
        if cur is None:
            return None
        while cur.child[0] is not None:
            cur = cur.child[0]
        return cur

    def print_tree(self):
        if self.root is not None:
            BTreePnt.print_tree_util(self.root, 0)

    def print_tree_util(self, node, depth):
        if node.child[len(node.pnt)] is not None:
            BTreePnt.print_tree_util(node.child[len(node.pnt)], depth + 1)
        for i in range(len(node.pnt) - 1, 0, -1):
            print('    ' * depth, end='')
            print('({},{})'.format(node.pnt[i][0], node.pnt[i][1]))
            if node.child[i] is not None:
                BTreePnt.print_tree_util(node.child[i], depth + 1)
        print('    ' * depth, end='')
        print('({},{})'.format(node.pnt[0][0], node.pnt[0][1]))
        if node.child[0] is not None:
            BTreePnt.print_tree_util(node.child[0], depth + 1)


if __name__ == '__main__':
    fn = 'input.txt'
    f = open(fn, 'r')
    datas = f.readlines()
    f.close()
    N_data_list = []
    for i in range(len(datas)):
        N_data_list.append(i + 1)
        datas[i] = int(datas[i])

    _23tree, _234tree = BTreePnt(3), BTreePnt(4)

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

