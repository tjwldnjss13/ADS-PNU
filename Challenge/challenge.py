from BinarySearchTree import *
from RedBlackTree import *
from BTree import *
from MergeSort import *
import copy

POINT_DICT = dict()


def get_table():
    return POINT_DICT


def read_file(fp):
    f = open(fp, 'r')
    lines = f.readlines()
    f.close()

    return lines


def range_search(bst_x, x_min, x_max, y_min, y_max):
    pass


def main():
    # ptn_dict = dict()
    # ptns_x = []
    range_tree_x = RedBlackTreePnt(0)

    fp = 'input.txt'
    pin = read_file(fp)

    for query in pin:
        q = query.split()

        if q[0] == '+':
            index, ptn = int(q[1]), (int(q[2]), int(q[3]))
            POINT_DICT[index] = ptn

            # ptns_x.append(ptn)
            # merge_sort_ptn(ptns_x, 0, 0, len(ptns_x) - 1)
            range_tree_x.insert(POINT_DICT[index])
            range_tree_x.print_tree()
            print('- - - - - - - - - - - - - - - - - - - - - -')
            range_tree_x.root.range_tree_y.print_tree()
        elif q[0] == '-':
            index = int(q[1])
            range_tree_x.delete(index)
            # del ptn_dict[i]
        elif q[0] == '?':
            ptn, r = (int(q[1]), int(q[2])), int(q[3])
            # ...

        print('-----------------------------------------------------')

    # print(POINT_DICT)
    # print(ptns_x)
    # range_tree_x.print_tree()
    # print('-------------------------------------------------')
    # range_tree_x.delete(ptns_dict[4])
    # range_tree_x.print_tree()
    # print('-------------------------------------------------')

    # range_tree_x.root.range_tree_y.print_tree()
    range_tree_x.root.left.range_tree_y.print_tree()



if __name__ == '__main__':
    main()
