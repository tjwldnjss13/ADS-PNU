from challenge import *


class Node:
    def __init__(self, index, pnt, color='b'):
        self.index = index
        self.pnt = pnt
        self.left = None
        self.right = None
        self.parent = None
        self.color = color
        self.depth = 0
        self.range = None
        self.range_tree_y = None


class RedBlackTreePnt:
    def __init__(self, xy_idx):
        self.root = None
        self.xy_idx = xy_idx
        self.N_pnt = 0

    def search(self, pnt):
        cur = self.root
        if cur is None:
            return None
        if cur.pnt[0] == pnt[0] and cur.pnt[1] == pnt[1]:
            return cur
        while cur is not None:
            if pnt[self.xy_idx] < cur.pnt[self.xy_idx]:
                cur = cur.left
            elif pnt[self.xy_idx] > cur.pnt[self.xy_idx]:
                cur = cur.right
            else:
                return cur

    def insert(self, index, pnt):
        if self.search(pnt) is not None:
            return
        if self.root is None:
            node = Node(index, pnt)
            # if self.xy_idx == 0:
            #     node.range_tree_y = RedBlackTreePnt(1)
            #     node.range_tree_y.insert(pnt)
            self.root = node
            self.N_pnt += 1
        else:
            if self.search(pnt) is None:
                cur = self.root
                parent = None
                while cur is not None:
                    parent = cur
                    if pnt[self.xy_idx] < cur.pnt[self.xy_idx]:
                        cur = cur.left
                    else:
                        cur = cur.right
                node = Node(index, pnt, 'r')
                # if self.xy_idx == 0:
                #     node.range_tree_y = RedBlackTreePnt(1)
                if pnt[self.xy_idx] < parent.pnt[self.xy_idx]:
                    parent.left = node
                else:
                    parent.right = node
                node.parent = parent
                # node.depth = parent.depth + 1
                self.N_pnt += 1

                # # Make tree of y
                # if self.xy_idx == 0:
                #     self.insert_to_sub_range_tree(pnt)

                # Reconstruct / Recolor conditions
                if node.parent.color == 'r':
                    self.balance(node)

                # Make tree of y
                # if self.xy_idx == 0:
                #     self.update_sub_range_tree()

    def insert_to_sub_range_tree(self, pnt):
        self.insert_to_sub_range_tree_util(self.root, pnt)

    def insert_to_sub_range_tree_util(self, cur, pnt, start=None, end=None):
        if cur.right is not None:
            self.insert_to_sub_range_tree_util(cur.right, pnt, start=cur.pnt[self.xy_idx], end=end)

        # Case : Root
        if start is None and end is None:
            cur.range_tree_y.insert(pnt)
        # Case : Right-most node
        elif start is not None and end is None:
            if pnt[self.xy_idx] >= start:
                cur.range_tree_y.insert(pnt)
        # Case : Left-most node
        elif start is None and end is not None:
            if pnt[self.xy_idx] <= end:
                cur.range_tree_y.insert(pnt)
        # Case : Internal node
        else:
            if start <= cur.pnt[self.xy_idx] <= end:
                cur.range_tree_y.insert(pnt)

        if cur.left is not None:
            self.insert_to_sub_range_tree_util(cur.left, pnt, start=start, end=cur.pnt[self.xy_idx])

    def delete(self, pnt):
        target = self.search(pnt)
        if target is None:
            return
        parent = target.parent
        if target is self.root:
            child_f = -1
        elif target is parent.left:
            child_f = 0
        else:
            child_f = 1

        target_color = target.color
        double_black_f = False

        # When target is a leaf node
        if target.left is None and target.right is None:
            double_black_f = True
            if child_f == 0:
                parent.left = None
            elif child_f == 1:
                parent.right = None

        # When target is an internal node
        elif target.left is not None and target.right is None:
            if self.xy_idx == 0:
                target.left.range_tree_y = target.range_tree_y
            if child_f == 0:
                parent.left = target.left
                parent.left.parent = parent
                if parent.left.color == 'b':
                    double_black_f = True
                parent.left.color = 'b'
            elif child_f == 1:
                parent.right = target.left
                parent.right.parent = parent
                if parent.right.color == 'b':
                    double_black_f = True
                parent.right.color = 'b'
        elif target.left is None and target.right is not None:
            if self.xy_idx == 0:
                target.right.range_tree_y = target.range_tree_y
            if child_f == 0:
                parent.left = target.right
                parent.left.parent = parent
                if parent.left.color == 'b':
                    double_black_f = True
                parent.left.color = 'b'
            elif child_f == 1:
                parent.right = target.right
                parent.right.parent = parent
                if parent.right.color == 'b':
                    double_black_f = True
                parent.right.color = 'b'
        else:
            pre, pre_depth = RedBlackTreePnt.get_predecessor(target)
            suc, suc_depth = RedBlackTreePnt.get_successor(target)

            # Replace target to successor/predecessor
            if pre_depth < suc_depth:
                if self.xy_idx == 0:
                    suc.range_tree_y = target.range_tree_y
                if suc.color == 'b':
                    double_black_f = True
                suc.color = 'b'
                self.replace_to_successor(target, suc)
            else:
                if self.xy_idx == 0:
                    pre.range_tree_y = target.range_tree_y
                if pre.color == 'b':
                    double_black_f = True
                pre.color = 'b'
                self.replace_to_predecessor(target, pre)

        # When target's color is red, just delete it
        if target_color == 'r':
            # self.update_sub_range_tree()
            return
        # When target's color is black
        else:
            if not double_black_f:
                # self.update_sub_range_tree()
                return

            if child_f == 0:
                sib = parent.right
            elif child_f == 1:
                sib = parent.left
            else:
                # self.update_sub_range_tree()
                return

            self.update_after_delete(target, parent, sib, child_f)
            # self.update_sub_range_tree()

    def update_after_delete(self, target, parent, sib, child_f):
        if parent is None:
            return

        if sib is None:
            return

        # When sibling's color is red
        if sib.color == 'r':
            sib.color = 'b'
            target.color = 'r'
            if child_f == 0:
                self.rotate_left(parent)
            elif child_f == 1:
                self.rotate_right(parent)

        # When sibling's color is black (complicated)
        else:
            # When target is parent's left child
            if child_f == 0:
                # When sibling's left and right are both black
                if (sib.left is None or (sib.left is not None and sib.left.color == 'b')) and (
                        sib.right is None or (sib.right is not None and sib.right.color == 'b')):
                    sib.color = 'r'
                    double_black_f = parent.color == 'b'
                    parent.color = 'b'
                    if double_black_f:
                        target = parent
                        parent = parent.parent

                        if target is self.root:
                            return
                        if target is parent.left:
                            child_f = 0
                            sib = parent.right
                        else:
                            child_f = 1
                            sib = parent.left

                        self.update_after_delete(target, parent, sib, child_f)

                # When siblings' left is red and right is black
                elif (sib.left is not None and sib.left.color == 'r') and (
                        sib.right is None or (sib.right is not None and sib.right.color == 'b')):
                    sib.color = 'r'
                    sib.left.color = 'b'
                    self.rotate_left(sib)

                # When sibling's right is red
                else:
                    sib.color = parent.color
                    parent.color, sib.right.color = 'b', 'b'
                    self.rotate_left(parent)

            # When target is parent;s right child
            elif child_f == 1:
                # When sibling's left and right are both black
                if (sib.left is None or (sib.left is not None and sib.left.color == 'b')) and (
                        sib.right is None or (sib.right is not None and sib.right.color == 'b')):
                    sib.color = 'r'
                    double_black_f = parent.color == 'b'
                    parent.color = 'b'
                    if double_black_f:
                        target = parent
                        parent = parent.parent

                        if target is self.root:
                            return
                        if target is parent.left:
                            child_f = 0
                            sib = parent.right
                        else:
                            child_f = 1
                            sib = parent.left

                        self.update_after_delete(target, parent, sib, child_f)

                # When siblings' left is black and right is red
                elif (sib.left is None or (sib.left is not None and sib.left.color == 'b')) and (
                        sib.right is not None and sib.right.color == 'b'):
                    sib.color = 'r'
                    sib.right.color = 'b'
                    self.rotate_right(sib)
                # When sibling's left is red
                else:
                    sib.color = parent.color
                    parent.color = 'b'
                    if sib.left is not None:
                        sib.left.color = 'b'
                    self.rotate_right(parent)

    def update_sub_range_tree(self):
        if self.root is None:
            return
        self.update_sub_range_tree_util(self.root, [])

    def update_sub_range_tree_util(self, node, parents):
        node.range_tree_y = RedBlackTreePnt(1)
        if node.right is not None:
            parents.append(node)
            self.update_sub_range_tree_util(node.right, parents)
            parents.pop(-1)
        node.range_tree_y.insert(node.pnt)
        for parent in parents:
            parent.range_tree_y.insert(node.pnt)
        if node.left is not None:
            parents.append(node)
            self.update_sub_range_tree_util(node.left, parents)
            parents.pop(-1)

    @staticmethod
    def make_sub_range_tree():
        pass

    def balance(self, node):
        # if node.depth < 2:
        if node.parent is self.root or node.parent is None:
            return
        parent = node.parent
        gparent = parent.parent
        uncle = None
        if parent is gparent.left:
            uncle = gparent.right
        elif parent is gparent.right:
            uncle = gparent.left

        if uncle is None or (uncle is not None and uncle.color == 'b'):
            self.reconstruct(node)
        elif uncle is not None and uncle.color == 'r':
            self.recolor(node)

    def reconstruct(self, node):
        parent = node.parent
        gparent = parent.parent
        if parent is None:
            return
        if parent is gparent.left:
            if node is parent.right:
                # left rotate
                parent = self.rotate_left(parent)
            # right rotate
            gparent = parent.parent
            gparent = self.rotate_right(gparent)

            # Recolor
            gparent.color = 'b'
            gparent.right.color = 'r'

        elif parent is gparent.right:
            if node is parent.left:
                # right rotate
                parent = self.rotate_right(parent)
            # left rotate
            gparent = parent.parent
            gparent = self.rotate_left(gparent)

            # Recolor
            gparent.color = 'b'
            gparent.left.color = 'r'

    def recolor(self, node):
        parent = node.parent
        gparent = parent.parent
        uncle = None
        if parent is gparent.left:
            uncle = gparent.right
        elif parent is gparent.right:
            uncle = gparent.left

        parent.color = 'b'
        uncle.color = 'b'
        if gparent is self.root:
            gparent.color = 'b'
        else:
            gparent.color = 'r'

            if gparent.parent.color == 'r':
                self.balance(gparent)

    def rotate_left(self, node):
        if node.right is None:
            return

        if node is self.root:
            child_f = -1
        else:
            parent_temp = node.parent
            if node is parent_temp.left:
                child_f = 0
            else:
                child_f = 1

        new_subroot = node.right
        if child_f == -1:
            self.root = new_subroot
            self.root.parent = None
        else:
            new_subroot.parent = parent_temp
            if child_f == 0:
                parent_temp.left = new_subroot
            elif child_f == 1:
                parent_temp.right = new_subroot
        sub = new_subroot.left

        new_subroot.left = node
        node.parent = new_subroot
        new_subroot.left.right = sub
        if sub is not None:
            sub.parent = new_subroot.left

        # self.reset_depth(new_subroot)

        return new_subroot

    def rotate_right(self, node):
        if node.left is None:
            return

        if node is self.root:
            child_f = -1
        else:
            parent_temp = node.parent
            if node is parent_temp.left:
                child_f = 0
            else:
                child_f = 1

        new_subroot = node.left
        if child_f == -1:
            self.root = new_subroot
            self.root.parent = None
        else:
            new_subroot.parent = parent_temp
            if child_f == 0:
                parent_temp.left = new_subroot
            elif child_f == 1:
                parent_temp.right = new_subroot
        sub = new_subroot.right

        new_subroot.right = node
        node.parent = new_subroot
        new_subroot.right.left = sub
        if sub is not None:
            sub.parent = new_subroot.right
        #
        self.reset_depth(new_subroot)

        return new_subroot

    def get_max(self):
        if self.root is None:
            return None
        cur = self.root
        while cur.right is not None:
            cur = cur.right
        return cur

    @staticmethod
    def get_predecessor(node):
        if node is None:
            return None
        pre = node.left
        depth = 0
        while pre.right is not None:
            pre = pre.right
            depth += 1

        return pre, depth

    @staticmethod
    def get_successor(node):
        if node is None:
            return None
        suc = node.right
        depth = 0
        while suc.left is not None:
            suc = suc.left
            depth += 1

        return suc, depth

    def replace_to_predecessor(self, target, pre):
        if target is pre.parent:
            pre.right = target.right
            if pre.right is not None:
                pre.right.parent = pre
        else:
            # pre_parent = pre.parent
            pre.left, pre.right = target.left, target.right
            if pre.left is not None:
                pre.left.parent = pre
            if pre.right is not None:
                pre.right.parent = pre
            pre.parent.right = None

        if target is self.root:
            pre.parent = None
            self.root = pre
        else:
            if target is target.parent.left:
                target.parent.left = pre
            else:
                target.parent.right = pre
            pre.parent = target.parent

    def replace_to_successor(self, target, suc):
        if target is suc.parent:
            suc.left = target.left
            if suc.left is not None:
                suc.left.parent = suc
        else:
            suc.left, suc.right = target.left, target.right
            if suc.left is not None:
                suc.left.parent = suc
            if suc.right is not None:
                suc.right.parent = suc
            suc.parent.left = None

        if target is self.root:
            suc.parent = None
            self.root = suc
        else:
            if target is target.parent.left:
                target.parent.left = suc
            else:
                target.parent.right = suc
            suc.parent = target.parent

    def reset_depth(self, node):
        if node is None:
            return
        self.reset_depth_util(node)

    def reset_depth_util(self, node):
        if node.parent is not None:
            node.depth = node.parent.depth + 1
        else:
            node.depth = 0
        if node.right is not None:
            self.reset_depth_util(node.right)
        if node.left is not None:
            self.reset_depth_util(node.left)

    def print_tree(self):
        if self.root is None:
            return
        self.print_tree_util(self.root, 0)

    @staticmethod
    def print_tree_util(node, depth):
        if node.right is not None:
            RedBlackTreePnt.print_tree_util(node.right, depth + 1)
        print(depth * '                   ', end='')
        print('({},{}):{}'.format(node.pnt[0], node.pnt[1], node.color))
        if node.left is not None:
            RedBlackTreePnt.print_tree_util(node.left, depth + 1)

