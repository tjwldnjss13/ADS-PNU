import random
import copy

MIN_PRIOR, MAX_PRIOR = 1, 10000000

class Treap:
    duplicated = 0

    class Node:
        def __init__(self, key=0):
            self.key = key
            self.priority = random.randint(MIN_PRIOR, MAX_PRIOR)
            self.parent = None
            self.left = None
            self.right = None
            self.depth = 0

    def __init__(self):
        self.root = None
        self.N_node = 0

    # Function to search the key
    def search(self, key):
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

    # Function to insert a new key in the Treap
    def insert(self, key):
        global duplicated

        new_node = self.Node(key)
        if self.root is None:
            self.root = new_node
            self.N_node += 1
            return
        if self.search(key) is not None:
            self.duplicated += 1
            return
        parent = None
        cur = self.root
        while cur is not None:
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                self.duplicated += 1
                return
        if key < parent.key:
            parent.left = new_node
        elif key > parent.key:
            parent.right = new_node
        new_node.parent = parent
        new_node.depth = parent.depth + 1
        self.self_balance_with_priority(new_node)
        self.N_node += 1

    # Function to balance the Treap with priority upward from a certain node
    def self_balance_with_priority(self, node):
        parent = node.parent
        while parent is not None:
            if node.priority > parent.priority:
                if node is parent.left:
                    balanced_node = self.right_rotate(parent)
                elif node is parent.right:
                    balanced_node = self.left_rotate(parent)
                node = balanced_node
                parent = node.parent
                Treap.adjust_depth(self)
            else:
                break

    # Function to balance the Treap with priority downward from a certain node
    def self_balance_with_priority_down(self, node):
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
                    cur = self.left_rotate(cur)
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

    # Function to rotate left a sub-Treap
    def left_rotate(self, subroot):
        parent = subroot.parent
        if parent is not None:
            if parent.left is subroot:
                childF = -1
            elif parent.right is subroot:
                childF = 1

        if subroot.right is not None:
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

        return new_subroot

    # Function to rotate right a sub-Treap
    def right_rotate(self, subroot):
        parent = subroot.parent
        if parent is not None:
            if parent.left is subroot:
                childF = -1
            elif parent.right is subroot:
                childF = 1

        if subroot.left is not None:
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

        return new_subroot

    # Function to delete the key
    def delete(self, key):
        target = self.search(key)
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

    # Function to split the Treap based on a certain key
    def split(self, key):
        cur = self.search_key(key)
        if cur is not None:
            prior_temp = cur.priority
            cur.priority = MAX_PRIOR + 1
            self.self_balance_with_priority(cur)

            t1, t2 = copy.deepcopy(self), copy.deepcopy(self)
            t1.root.right, t2.root.left = None, None
            t1.root.priority = prior_temp
            t2.delete_key(t2.root.key)
            t1.self_balance_with_priority_down(t1.root)
            t2.self_balance_with_priority_down(t2.root)

            return t1, t2
        else:
            return None, None

    # Function to merge 2 Treaps
    @staticmethod
    def merge(t1, t2):
        if t1 is None and t2 is None:
            return None
        elif t1 is None and t2 is not None:
            return t2
        elif t1 is not None and t2 is None:
            return t1
        else:
            t1_max, t1_min = t1.root, t1.root
            while t1_max.right is not None:
                t1_max = t1_max.right
            while t1_min.left is not None:
                t1_min = t1_min.left

            t2_max, t2_min = t2.root, t2.root
            while t2_max.right is not None:
                t2_max = t2_max.right
            while t2_min.left is not None:
                t2_min = t2_min.left

            if t1_max.key < t2_min.key:
                t = Treap()
                mid = (t1_max.key + t2_min.key) / 2
                t.insert(mid)
                t.root.left = copy.deepcopy(t1.root)
                t.root.right = copy.deepcopy(t2.root)
                t.delete(mid)
                Treap.adjust_depth(t)
                t.N_node = t1.N_node + t2.N_node
                return t
            elif t2_max.key < t1_min.key:
                t = Treap()
                mid = (t1_min.key + t2_max.key) / 2
                t.insert(mid)
                t.root.left = copy.deepcopy(t2.root)
                t.root.right = copy.deepcopy(t1.root)
                t.delete(mid)
                Treap.adjust_depth(t)
                t.N_node = t1.N_node + t2.N_node
                return t
            else:
                print('Not appropriate condition :(')
                return None

    # Function to decrease depths of the nodes in a sub-Treap
    @staticmethod
    def dec_depth(subroot):
        Treap.dec_depth_util(subroot)

    @staticmethod
    def dec_depth_util(node):
        if node.right is not None:
            Treap.dec_depth_util(node.right)
        node.depth -= 1
        if node.left is not None:
            Treap.dec_depth_util(node.left)

    # Function to increase depths of the nodes in a sub-Treap
    @staticmethod
    def inc_depth(subroot):
        Treap.inc_depth_util(subroot)

    @staticmethod
    def inc_depth_util(node):
        if node.right is not None:
            Treap.inc_depth_util(node.right)
        node.depth += 1
        if node.left is not None:
            Treap.inc_depth_util(node.left)

    # Function to reset depths of the nodes in a Treap
    @staticmethod
    def adjust_depth(t):
        t.root.depth = 0
        Treap.adjust_depth_util(t.root)

    @staticmethod
    def adjust_depth_util(node):
        if node.left is not None:
            node.left.depth = node.depth + 1
            Treap.adjust_depth_util(node.left)
        if node.right is not None:
            node.right.depth = node.depth + 1
            Treap.adjust_depth_util(node.right)

    @staticmethod
    def print_treap(t):
        Treap.print_treap_util(t.root)

    @staticmethod
    def print_treap_util(cur):
        if cur.right is not None:
            Treap.print_treap_util(cur.right)
        for i in range(cur.depth):
            print('             ', end='')
        print('{}({})'.format(cur.key, cur.priority))
        if cur.left is not None:
            Treap.print_treap_util(cur.left)


if __name__ == '__main__':
    t1 = Treap()
    n = 20

    print('Insert {} datas'.format(n))
    for i in range(n):
        t1.insert(key=random.randint(1, n))

    # Split
    # target = random.randint(1, n)
    # if t1.search_key(target) is not None:
    #     print('Split with {}'.format(target))
    #     t1_1, t1_2 = t1.split(target)
    #     print('[1]')
    #     t1_1.print_treap()
    #     print('[2]')
    #     t1_2.print_treap()
    # else:
    #     print('{} is not here :('.format(target))

    # Merge
    t2 = Treap()

    for i in range(n):
        t2.insert(key=random.randint(2*n, 3*n))

    Treap.print_treap(t1)
    print('[T1] Total # of key : {}'.format(t1.N_node))
    print('[T1] # of duplicated key (not inserted) : {}'.format(t1.duplicated))

    print()

    Treap.print_treap(t2)
    print('[T2] Total # of key : {}'.format(t2.N_node))
    print('[T2] # of duplicated key (not inserted) : {}'.format(t2.duplicated))

    print('Merge T1 & T2')
    t3 = Treap.merge(t1, t2)
    if t3 is not None:
        Treap.print_treap(t3)
        print(t3.N_node)


