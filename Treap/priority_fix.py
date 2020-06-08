import random
import copy

MIN_PRIOR, MAX_PRIOR = 1, 10000000
duplicated = 0

class Treap:
    class Node:
        def __init__(self, key=0, priority=0):
            self.key = key
            self.priority = priority
            self.parent = None
            self.left = None
            self.right = None
            self.depth = 0

    def __init__(self):
        self.root = None
        self.N_node = 0

    def search_key(self, key):
        cur = self.root
        while True:
            if key < cur.key and cur.left is not None:
                cur = cur.left
            elif key > cur.key and cur.right is not None:
                cur = cur.right
            elif key is cur.key:
                return cur
            else:
                return None

    def insert_key(self, key, priority):
        global duplicated

        print('----- Inserting {} -----'.format(key))
        new_node = self.Node(key, priority)
        if self.root is None:
            self.root = new_node
            self.N_node += 1
            return
        if self.search_key(key) is not None:
            duplicated += 1
            return
        parent = None
        cur = self.root
        while cur is not None:
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
        if key < parent.key:
            parent.left = new_node
        elif key > parent.key:
            parent.right = new_node
        new_node.parent = parent
        new_node.depth = parent.depth + 1
        self.self_balance_with_priority(new_node)
        self.N_node += 1

    def self_balance_with_priority(self, node):
        parent = node.parent
        while parent is not None:
            if node.priority > parent.priority:
                if node is parent.left:
                    balanced_node = self.right_rotate(parent)
                    # self.self_balance_with_priority(balanced_node)
                elif node is parent.right:
                    balanced_node = self.left_rotate(parent)
                    # self.self_balance_with_priority(balanced_node)
                node = balanced_node
                parent = node.parent
            else:
                break

    def self_balance_with_priority_down(self, node):
        print('[Down-Self-Balance function]')
        cur = node
        while cur is not None:
            left, right = cur.left, cur.right
            if left is None and right is None:
                break
            elif left is not None and right is None:
                if cur.priority < left.priority:
                    cur = self.right_rotate(cur)
                    cur = cur.right
                else:
                    break
            elif left is None and right is not None:
                if cur.priority < right.priority:
                    cur = self.right_rotate(cur)
                    cur = cur.left
                else:
                    break
            else:
                if left.priority < right.priority:
                    child = right
                    rotateF = -1
                else:
                    child = left
                    rotateF = 1
                if cur.priority < child.priority:
                    if rotateF is 1:
                        cur = self.right_rotate(cur)
                        cur = cur.right
                    elif rotateF is -1:
                        cur = self.left_rotate(cur)
                        cur = cur.left
                else:
                    break

    def left_rotate(self, subroot):
        parent = subroot.parent
        if parent is not None:
            if parent.left is subroot:
                childF = -1
            elif parent.right is subroot:
                childF = 1

        child_temp = subroot.right.left
        if child_temp is not None:
            child_temp.parent = subroot
        new_subroot = subroot.right
        subroot.parent = new_subroot
        new_subroot.left = subroot
        new_subroot.left.right = child_temp

        new_subroot.parent = parent
        if parent is not None:
            if childF is -1:
                parent.left = new_subroot
            elif childF is 1:
                parent.right = new_subroot
        else:
            self.root = new_subroot

        new_subroot.depth -= 1
        if new_subroot.right is not None:
            self.dec_depth_util(new_subroot.right)
        new_subroot.left.depth += 1
        if new_subroot.left.left is not None:
            self.inc_depth(new_subroot.left.left)

        return new_subroot

    def right_rotate(self, subroot):
        parent = subroot.parent
        if parent is not None:
            if parent.left is subroot:
                childF = -1
            elif parent.right is subroot:
                childF = 1

        child_temp = subroot.left.right
        if child_temp is not None:
            child_temp.parent = subroot
        new_subroot = subroot.left
        subroot.parent = new_subroot
        new_subroot.right = subroot
        new_subroot.right.left = child_temp

        new_subroot.parent = parent
        if parent is not None:
            if childF is -1:
                parent.left = new_subroot
            elif childF is 1:
                parent.right = new_subroot
        else:
            self.root = new_subroot

        new_subroot.depth -= 1
        if new_subroot.left is not None:
            self.dec_depth_util(new_subroot.left)
        new_subroot.right.depth += 1
        if new_subroot.right.right is not None:
            self.inc_depth(new_subroot.right.right)

        return new_subroot

    def delete_key(self, key):
        print('[Delete function]')
        target = self.search_key(key)
        if target is not None:
            # Case 1 : Target is a leaf node (no child)
            if target.right is None and target.left is None:
                if target is self.root:
                    self.root = None
                else:
                    if target.parent is not None:
                        parent = target.parent
                        if target is parent.left:
                            parent.left = None
                        elif target is parent.right:
                            parent.right = None

            # Case 2 : Target only has right child
            elif target.left is None and target.right is not None:
                self.dec_depth(target.right)
                if target is self.root:
                    self.root = target.right
                    self.root.parent = None
                else:
                    parent = target.parent
                    if parent is not None:
                        if target is parent.left:
                            parent.left = target.right
                            parent.left.parent = parent
                        elif target is parent.right:
                            parent.right = target.right
                            parent.right.parent = parent
            # Case 3 : Target only has left child
            elif target.left is not None and target.right is None:
                self.dec_depth(target.left)
                if target is self.root:
                    self.root = target.left
                    self.root.parent = None
                else:
                    parent = target.parent
                    if parent is not None:
                        if target is parent.left:
                            parent.left = target.left
                            parent.left.parent = parent
                        elif target is parent.right:
                            parent.right = target.left
                            parent.right.parent = parent

            # Case 4 : Target has both child
            else:
                left_max, right_min = target.left, target.right

                while left_max.right is not None:
                    left_max = left_max.right
                while right_min.left is not None:
                    right_min = right_min.left

                if left_max.depth <= right_min.depth:
                    parent_temp = right_min.parent
                    child_temp = right_min.right
                    if parent_temp is target:
                        target.right = child_temp
                    else:
                        parent_temp.left = child_temp
                    if child_temp is not None:
                        child_temp.parent = parent_temp
                        self.dec_depth(child_temp)
                    target.key, target.priority = right_min.key, right_min.priority
                else:
                    parent_temp = left_max.parent
                    child_temp = left_max.left
                    if parent_temp is target:
                        target.left = child_temp
                    else:
                        parent_temp.right = child_temp
                    if child_temp is not None:
                        child_temp.parent = parent_temp
                        self.dec_depth(child_temp)
                    target.key, target.priority = left_max.key, left_max.priority

                self.self_balance_with_priority_down(target)

            self.N_node -= 1
        else:
            return

    def split_treap(self, key):
        cur = self.search_key(key)
        if cur is not None:
            prior_temp = cur.priority
            cur.priority = MAX_PRIOR + 1
            self.self_balance_with_priority(cur)

            t1, t2 = copy.deepcopy(self), copy.deepcopy(self)
            t1.root.right, t2.root.left = None, None
            t1.root.priority, t2.root.priority = prior_temp, prior_temp
            t1.self_balance_with_priority_down(t1.root)
            t2.self_balance_with_priority_down(t2.root)

            return t1, t2
        else:
            return None

    def merge_treaps(self):
        pass

    def dec_depth(self, subroot):
        self.dec_depth_util(subroot)

    def dec_depth_util(self, node):
        if node.right is not None:
            self.dec_depth_util(node.right)
        node.depth -= 1
        if node.left is not None:
            self.dec_depth_util(node.left)

    def inc_depth(self, subroot):
        self.inc_depth_util(subroot)

    def inc_depth_util(self, node):
        if node.right is not None:
            self.inc_depth_util(node.right)
        node.depth += 1
        if node.left is not None:
            self.inc_depth_util(node.left)

    def print_treap(self):
        self.print_treap_util(self.root)

    def print_treap_util(self, cur):
        if cur.right is not None:
            self.print_treap_util(cur.right)
        for i in range(cur.depth):
            print('             ', end='')
        print('{}({})'.format(cur.key, cur.priority))
        if cur.left is not None:
            self.print_treap_util(cur.left)


if __name__ == '__main__':
    t = Treap()
    n = 260

    # for i in range(7):
    #     t.insert_key(key=random.randint(1, 10))

    for i in range(1, n + 1):
        t.insert_key(i, n - i);

    # t.insert_key(6, 97)
    # t.insert_key(5, 82)
    # t.insert_key(8, 86)
    # t.insert_key(2, 23)
    # t.insert_key(10, 44)
    # t.insert_key(12, 15)

    t.print_treap()

    # print('----- Split treap -----')
    # t1, t2 = t.split_treap(8)
    #
    # t1.print_treap()
    # t2.print_treap()

    # print('----- Delete root -----')
    # t.delete_key(t.root.key)
    # t.print_treap()

    print()
    print(t.N_node)
    print(duplicated)