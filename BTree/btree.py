import copy


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

        # If selected leaf is root
        if node is self.root:
            # Make new root
            root_new = self.create_node(node_temp.key.pop(int((len(node_temp.key) - 1) / 2)))

            # Set new root's children
            root_new.child[0] = self.create_node(key=copy.deepcopy(node_temp.key[:int(len(node_temp.key) / 2)]))
            root_new.child[1] = self.create_node(key=copy.deepcopy(node_temp.key[int(len(node_temp.key) / 2):]))
            # for i in range(len(root_new.key) + 1):
            #     root_new.child[i].parent = root_new
            for i in range(len(root_new.child[0].key) + 1):
                root_new.child[0].child[i] = sub_child.pop(0)
            for i in range(len(root_new.child[1].key) + 1):
                root_new.child[1].child[i] = sub_child.pop(0)
            self.root = root_new
            return

        parent = self.get_parent(node)
        key_mid = node_temp.key.pop(int((len(node_temp.key) - 1) / 2))

        # 부모 노드에 자리가 남아있을 때
        if len(parent.key) < self.degree - 1:
            # 나누는 노드의 중간값을 부모 노드에 추가
            parent.key.append(key_mid)
            parent.key.sort()

            # 노드를 나눠서 부모 노드의 자식으로 추가
            child_i = parent.key.index(key_mid)
            parent.child[child_i] = self.create_node(key=copy.deepcopy(node_temp.key[:int(len(node.key) / 2)]))
            parent.child.insert(child_i + 1, self.create_node(key=copy.deepcopy(node_temp.key[(int(len(node.key) / 2)):])))
            while len(parent.child) > self.degree:
                parent.child.pop(-1)
            for i in range(child_i, child_i + 2):
                for j in range(len(parent.child[i].key) + 1):
                    parent.child[i].child[j] = sub_child.pop(0)

        # 부모 노드에 자리가 안 남아있을 때
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
            if len(target.key) == 1:
                if target is parent.child[0]:
                    sib = parent.child[1]
                    if len(sib.key) == 1:
                        gparent = self.get_parent(parent)
                        parent_i = gparent.child.index(parent)
                        sib.key.insert(0, parent.key.pop(0))
                        if parent is self.root:
                            self.root = sib
                            self.N_key -= 1
                            return
                        if len(parent.key) == 0:
                            gparent.child[parent_i] = sib
                            self.N_key -= 1
                            return
                        parent.child.pop(0)
                        while len(parent.child) < 5:
                            parent.child.append(None)
                        self.N_key -= 1
                        return
                    else:
                        target.key[0] = parent.key.pop(0)
                        parent.key.insert(0, sib.key.pop(0))
                        self.N_key -= 1
                        return
                else:
                    child_i = parent.child.index(target)
                    sib = parent.child[child_i - 1]
                    if len(sib.key) == 1:
                        gparent = self.get_parent(parent)
                        parent_i = gparent.child.index(parent)
                        sib.key.append(parent.key.pop(child_i - 1))
                        if parent is self.root:
                            self.root = sib
                            self.N_key -= 1
                            return
                        if len(parent.key) == 0:
                            gparent.child[parent_i] = sib
                            self.N_key -= 1
                            return
                        parent.child.pop(child_i)
                        while len(parent.child) < self.degree:
                            parent.child.append(None)
                        self.N_key -= 1
                        return
                    else:
                        target.key[0] = parent.key.pop(child_i - 1)
                        parent.key.insert(child_i - 1, sib.key.pop(-1))
                        self.N_key -= 1
                        return

            # Case 2-2
            else:
                target.key.pop(target.key.index(key))
                self.N_key -= 1
                return
        # Case 3
        pre = self.get_predecessor(key)
        suc = self.get_successor(key)
        key_i = target.key.index(key)

        if len(pre.key) > 1:
            target.key[key_i] = pre.key.pop(-1)
            self.N_key -= 1
            return
        elif len(suc.key) > 1:
            target.key[key_i] = suc.key.pop(0)
            self.N_key -= 1
            return
        else:
            key_temp = pre.key[0]
            self.delete(key_temp, pre)
            target = self.search(key)
            key_i = target.key.index(key)
            target.key[key_i] = key_temp
            return

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
