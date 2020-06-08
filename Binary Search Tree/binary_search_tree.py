
class BST:
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.left = None
            self.right = None
            self.depth = 0

    def __init__(self, data=None):
        self.root = self.Node(data)

    def search(self, data, cur):
        print('Searching ' + str(data) + '...')
        if self.root.data == None:
            return None
        temp = cur
        if temp != None:
            if data < temp.data:
                self.search(data, temp.left)
            elif data > temp.data:
                self.search(data, temp.right)
            else:
                print('    Searching done')
                return temp
        print('    Failed to search ' + str(data))
        return None

    def insert(self, data):
        print('Inserting ' + str(data) + '...')
        if self.search(data, self.root) == None:
            if self.root.data == None:
                self.root.data = data
                print('    Inserted to the root')
                return self.root
            node = self.Node(data)
            parent = None
            current = self.root
            while current != None:
                parent = current
                if data < current.data:
                    current = current.left
                else:
                    current = current.right

            if data < parent.data:
                parent.left = node
                node.depth = parent.depth + 1
            else:
                parent.right = node
                node.depth = parent.depth + 1
            print('    Inserting done')
            return node
        print('    Failed to insert ' + str(data) + ' (Already exists)')
        return None

    def print_tree_util(self, cur):
        if cur.right != None:
            self.print_tree_util(cur.right)
        print('      ' * cur.depth, end='')
        print(cur.data)
        if cur.left != None:
            self.print_tree_util(cur.left)

    def print_tree(self):
        self.print_tree_util(self.root)


def main():
    bst = BST()

    bst.insert(100)
    bst.insert(16)
    bst.insert(192)
    bst.insert(5328)
    bst.insert(51)
    bst.insert(7)

    bst.print_tree()


if __name__ == '__main__':
    main()