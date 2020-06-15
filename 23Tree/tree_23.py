import copy

class Tree23:
    class Node:
        def __init__(self, key):
            if type(key) == list:
                self.key = key
            else:
                self.key = [key]
            self.child = []
            self.parent = None

    def __init__(self, degree=3):
        self.root = None
        self.degree = degree

    def create_node(self, key):
        node = self.Node(key)
        for i in range(self.degree):
            node.child.append(None)

        return node

    def search(self, key):
        if self.root is None:
            return None
        cur = self.root
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
        return None

    def insert(self, key):
        if self.search(key) is not None:
            return
        if self.root is None:
            self.root = self.create_node(key)
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
                return

            for i in range(1, len(cur.key) - 1):
                if cur.key[i - 1] < key < cur.key[i]:
                    cur.key.insert(i, key)
                    return
            if key > cur.key[-1]:
                cur.key.append(key)
                return
        else:
            self.split(cur, key)

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
            for i in range(len(root_new.key) + 1):
                root_new.child[i].parent = root_new
            self.root = root_new
            return

        parent = node.parent
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
            child_i = parent.child.index(node)
            sub_child_new = []
            for i in range(self.degree + 1):
                if i < child_i:
                    sub_child_new.append(parent.child[i])
                elif i == child_i:
                    sub_child_new.append(node1)
                    sub_child_new.append(node2)
                else:
                    sub_child_new.append(parent.child[i + 1])
            self.split(parent, key_mid, sub_child)

    @staticmethod
    def print_tree(tree):
        Tree23.print_tree_util(tree.root, 0)

    @staticmethod
    def print_tree_util(node, depth):
        if node.child[len(node.key)] is not None:
            Tree23.print_tree_util(node.child[len(node.key)], depth + 1)
        for i in range(len(node.key) - 1, 0, -1):
            print('    ' * depth, end='')
            print(node.key[i])
            if node.child[i + 1] is not None:
                Tree23.print_tree_util(node.child[i + 1], depth + 1)
        print('    ' * depth, end='')
        print(node.key[0])
        if node.child[0] is not None:
            Tree23.print_tree_util(node.child[0], depth + 1)
